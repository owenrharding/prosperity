from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
import statistics as st

class Trader:

    # Define position limits for each product.
    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}

    STARFRUIT_ORDER_FLAGS = {'BUY': False, 'SELL': False}

    # Define price history dictionaries for each product. These will store every historical acceptable price calculated by the algorithm.
    # These are stored in dictionaries, where timestamp is the key, and the acceptable price is the value.
    PRICE_HISTORY = {'AMETHYSTS': {}, 'STARFRUIT': {}}

    # Stored averages of price histories over a short and long term time frame at each timestamp
    SHORT_SMA_HISTORY = {'STARFRUIT': {}}
    LONG_SMA_HISTORY = {'STARFRUIT': {}}
    SHORT_WINDOW = 10
    LONG_WINDOW = 25

    """
    Updates price history arrays stored in Trader class.
    """
    def update_price_history(self, product: str, acceptable_price: float, state: TradingState):
        # Add acceptable price to corresponding product in PRICE_HISTORY dictionary
        if product in self.PRICE_HISTORY:
            self.PRICE_HISTORY[product][state.timestamp] = acceptable_price
    
    """
    Updates history of averages in certain scopes (long and short).
    """
    def update_sma_history(self, product: str, state: TradingState):
        if product in self.SHORT_SMA_HISTORY:
            # If the amount of historical values is greater than the window, then calculate based off the window
            if len(self.PRICE_HISTORY[product]) > self.SHORT_WINDOW:
                short_term_prices = list(self.PRICE_HISTORY[product].values())[-self.SHORT_WINDOW:]
            # Else calculate based on the values which have been saved up until now.
            # ie. If window is 50, but there are only 38 values, the sma for this window will be calculated using the current 38
            else:
                short_term_prices = list(self.PRICE_HISTORY[product].values())
            # Calculate mean
            self.SHORT_SMA_HISTORY[product][state.timestamp] = st.mean(short_term_prices)

            # Same logic as above
            if len(self.PRICE_HISTORY[product]) > self.LONG_WINDOW:
                long_term_prices = list(self.PRICE_HISTORY[product].values())[-self.LONG_WINDOW:]
            else:
                long_term_prices = list(self.PRICE_HISTORY[product].values())
            self.LONG_SMA_HISTORY[product][state.timestamp] = st.mean(long_term_prices)
    
    """
    Returns the predicted value of a dependent variable at an increment of an independent
    variable based on simple linear regression.
    It's assumed that the dictionary of data given to this function has the keys as the independent variable and the values
    as the dependent variable.
    It's pretty much assumed that the indepdenent variable is the timestamp and the dependent variable is the price.
    """
    def calculate_linear_regression(self, data: dict, scope: int, x_value: int):
        # Get list of (timestamp, price) tuples
        data_tuples = list(data.items())

        # Get the current scope number of elements from the end of the list
        current_scope_data = data_tuples[-scope:] # Array slicing, not sure if I've done it right

        # Extract timestamps and prices from the current scope amount of data
        # x_data is timestamps, y_data is prices
        x_data = np.array([item[0] for item in current_scope_data]) # Had to get ChatGPT to help me with this one :(
        y_data = np.array([item[1] for item in current_scope_data])
        n = np.size(x_data)

        x_mean = np.mean(x_data)
        y_mean = np.mean(y_data)

        # Just plugging numbers into formula
        Sxy = np.sum(x_data*y_data)- n*x_mean*y_mean 
        Sxx = np.sum(x_data*x_data)-n*x_mean*x_mean 

        m = Sxy/Sxx 
        c = y_mean-m*x_mean 

        # Make a prediction, using y = mx + c
        y_pred = m * x_value + c
        return y_pred

    def reset_starfruit_flags(self):
        self.STARFRUIT_ORDER_FLAGS['BUY'] = False 
        self.STARFRUIT_ORDER_FLAGS['SELL'] = False 

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

		# Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:

            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            # Get current position on respective product.
            current_position = state.position.get(product, 0)
            # Reset starfruit buy and sell flags from last trading state
            self.reset_starfruit_flags()
            
            # Determine max volume that can be bought/sold.
            max_buy_volume = self.POSITION_LIMIT[product] - current_position
            max_sell_volume = self.POSITION_LIMIT[product] + current_position

            # Get values with greatest trading volume (GTV).
            gtv_ask_price = list(order_depth.sell_orders.items())[-1][0]
            gtv_bid_price = list(order_depth.buy_orders.items())[-1][0]
            
            # Calculate acceptable price using most traded values.
            median_price = int((gtv_ask_price + gtv_bid_price) / 2)


            if product == 'STARFRUIT':
                ### LINEAR REGRESSION ###
                #print("***LINEAR REGRESSION***")
                #regression_scopes = [10, 50, 250, 500]
                #FUTURE_PREDICTION = 20
                #FUTURE_TIMESTAMP = state.timestamp + (100 * FUTURE_PREDICTION)
                #ERROR_VALUE = 0.0005
                #for scope in regression_scopes:
                #    lr_price = None
                #    if len(self.PRICE_HISTORY[product]) > scope:
                #        lr_price = self.calculate_linear_regression(self.PRICE_HISTORY[product], scope, FUTURE_TIMESTAMP)
                #    if lr_price is None:
                #        continue;
                #    print(scope, "predicts that", FUTURE_PREDICTION, "states from now at timestamp", FUTURE_TIMESTAMP, "the mid price will be:", lr_price, ".")

                #    if lr_price <= acceptable_price*(1+ERROR_VALUE) and lr_price >= acceptable_price*(1-ERROR_VALUE):
                #        print("The price is holding (+-", ERROR_VALUE*100, "%)")
                #    elif lr_price > acceptable_price*(1+ERROR_VALUE):
                #        print("The price is on the way up.\n")
                #    else: # lr_price < acceptable_price*0.99
                #        print("The price is on the way down.\n")
                #    
                #print("Current Acceptable Price for timestamp", state.timestamp, "is:", acceptable_price)

                ### SIMPLE MOVING AVERAGE ###
                print("***SIMPLE MOVING AVERAGE***")
                # You need to first determine a price in order to determine whether you should 
                # buy or sell using simple moving average at said acceptable price
                self.update_price_history(product, median_price, state)
                self.update_sma_history(product, state)

                if len(self.LONG_SMA_HISTORY[product]) < self.LONG_WINDOW:
                    self.STARFRUIT_ORDER_FLAGS['BUY'] = True
                    self.STARFRUIT_ORDER_FLAGS['SELL'] = True

                # Extract data from Short SMA
                short_sma_list = list(self.SHORT_SMA_HISTORY[product].items())
                # Find most recent and second most recent values to find gradient
                current_short_sma_timestamp, current_short_sma = short_sma_list[-1]
                prev_short_sma_timestamp, prev_short_sma = short_sma_list[-2]
                # Calculating rise over run
                short_sma_gradient = (current_short_sma - prev_short_sma) / (current_short_sma_timestamp - prev_short_sma_timestamp)

                # Extract data from Long SMA
                long_sma_list = list(self.LONG_SMA_HISTORY[product].items())
                # Find most recent and second most recent values to find gradient
                current_long_sma_timestamp, current_long_sma = long_sma_list[-1]
                prev_long_sma_timestamp, prev_long_sma = long_sma_list[-2]
                # Calculating rise over run
                long_sma_gradient = (current_long_sma - prev_long_sma) / (current_long_sma_timestamp - prev_long_sma_timestamp)

                print("Short Term SMA:", current_short_sma)
                #print("Short Term SMA GRADIENT is:", short_sma_gradient)
                print("Long Term SMA:", current_long_sma)
                #print("Long Term SMA GRADIENT is:", long_sma_gradient)

                ### BUY/SELL LOGIC BASED OFF SMA ###
                if (current_short_sma > current_long_sma) and (prev_long_sma > prev_short_sma): # Intersection with short SMA going from below to above long
                    # BUY
                    self.STARFRUIT_ORDER_FLAGS['BUY'] = True
                    print("BUY FLAG SET.")
                if (current_long_sma > current_short_sma) and (prev_short_sma > prev_long_sma): # Intersection with short SMA going from above to below long
                    # SELL
                    self.STARFRUIT_ORDER_FLAGS['SELL'] = True
                    print("SELL FLAG SET.")


            acceptable_price = median_price


            if product == 'STARFRUIT':
                ### BUY ###
                if len(order_depth.sell_orders) != 0:
                    if self.STARFRUIT_ORDER_FLAGS['BUY'] == True:
                        print("STARFRUIT BUY TRUE")
                        for price, amount in order_depth.sell_orders.items(): # Loop through each sell order.
                            if int(price) < acceptable_price: # Compare price against acceptable price to determine
                                if max_buy_volume >= amount: # Check if volume can be bought, without exceeding position limits.
                                    print("BUY", str(-amount) + "x", product, price)
                                    orders.append(Order(product, price, -amount))
                                else: # If position limit is exceeded, purchase quantity at maximum allowable volume.
                                    print("BUY", str(-max_buy_volume) + "x", product, price)
                                    orders.append(Order(product, price, -max_buy_volume))
            
                ### SELL ###
                # Buy orders use same logic as sell orders.
                if len(order_depth.buy_orders) != 0:
                    if self.STARFRUIT_ORDER_FLAGS['SELL'] == True:
                        print("STARFRUIT SELL TRUE")
                        for price, amount in order_depth.buy_orders.items():
                            if int(price) > acceptable_price:
                                if max_sell_volume >= amount:
                                    print("SELL", str(amount) + "x", product, price)
                                    orders.append(Order(product, price, -amount))
                                else:
                                    print("SELL", str(max_sell_volume) + "x", product, price)
                                    orders.append(Order(product, price, -max_sell_volume))
            else:
                ### BUY ###
                if len(order_depth.sell_orders) != 0:
                    for price, amount in order_depth.sell_orders.items(): # Loop through each sell order.
                        if int(price) < acceptable_price: # Compare price against acceptable price to determine
                            if max_buy_volume >= amount: # Check if volume can be bought, without exceeding position limits.
                                print("BUY", str(-amount) + "x", product, price)
                                orders.append(Order(product, price, -amount))
                            else: # If position limit is exceeded, purchase quantity at maximum allowable volume.
                                print("BUY", str(-max_buy_volume) + "x", product, price)
                                orders.append(Order(product, price, -max_buy_volume))
            
                ### SELL ###
                # Buy orders use same logic as sell orders.
                if len(order_depth.buy_orders) != 0:
                    for price, amount in order_depth.buy_orders.items():
                        if int(price) > acceptable_price:
                            if max_sell_volume >= amount:
                                print("SELL", str(amount) + "x", product, price)
                                orders.append(Order(product, price, -amount))
                            else:
                                print("SELL", str(max_sell_volume) + "x", product, price)
                                orders.append(Order(product, price, -max_sell_volume))

            result[product] = orders

        traderData = "SAMPLE" 
        
        conversions = 1
        return result, conversions, traderData