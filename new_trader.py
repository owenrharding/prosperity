from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
import statistics as st

class Trader:

    # Define position limits for each product.
    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}

    # Define historical data arrays. This will store previously calculated acceptable prices and the corresponding timestamps.
    PRICE_HISTORY = {'AMETHYSTS': {}, 'STARFRUIT': {}}# Got this from stack overflow, not sure if it works.

    def update_price_history(self, product: str, acceptable_price: float, state: TradingState):
        # Add acceptable price to corresponding product in PRICE_HISTORY dictionary
        if product in self.PRICE_HISTORY:
            product_dict = self.PRICE_HISTORY[product]
            product_dict[state.timestamp] = acceptable_price
    
    """
    A modular function that returns the predicted value of a dependent variable at an increment of an independent
    variable based on simple linear regression.
    It's assumed that the dictionary of data given to this function has the keys as the independent variable and the values
    as the dependent variable.
    It's pretty much assumed that the indepdenent variable is the timestamp and the dependent variable is the price.
    """
    def calculate_linear_regression(self, data: dict, scope: int, timestamp: int):
        # Get list of (timestamp, price) tuples
        data_tuples = list(data.items())

        # Get the last scope number of elements from the end of the list
        last_scope_data = data_tuples[-scope:]

        # Extract timestamps and prices from the last scope data
        x_data = np.array([item[0] for item in last_scope_data])
        y_data = np.array([item[1] for item in last_scope_data])

        n = np.size(x_data)

        x_mean = np.mean(x_data)
        y_mean = np.mean(y_data)

        Sxy = np.sum(x_data*y_data)- n*x_mean*y_mean 
        Sxx = np.sum(x_data*x_data)-n*x_mean*x_mean 

        a = Sxy/Sxx 
        b = y_mean-a*x_mean 

        y_pred = a * timestamp + b
        return y_pred

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
            
            # Determine max volume that can be bought/sold.
            max_buy_volume = self.POSITION_LIMIT[product] - current_position
            max_sell_volume = self.POSITION_LIMIT[product] + current_position

            if len(order_depth.sell_orders) != 0:
                ask_sum = 0
                ask_vol = 0
                for i in range(len(order_depth.sell_orders)):
                    ask, ask_amount = list(order_depth.sell_orders.items())[i]
                    ask_sum += int(ask) * int(ask_amount)
                    ask_vol += int(ask_amount)
                ask_avg = ask_sum / ask_vol if ask_vol != 0 else 0
            
            # Determine average bid price across orders and their corresponding amounts
            if len(order_depth.buy_orders) != 0:
                bid_sum = 0
                bid_vol = 0
                for i in range(len(order_depth.buy_orders)):
                    bid, bid_amount = list(order_depth.buy_orders.items())[i]
                    bid_sum += int(bid) * int(bid_amount)
                    bid_vol += int(bid_amount)
                bid_avg = bid_sum / bid_vol if bid_vol != 0 else 0

            # Get values with greatest trading volume (GTV).
            gtv_ask_price = list(order_depth.sell_orders.items())[-1][0]
            gtv_bid_price = list(order_depth.buy_orders.items())[-1][0]
            
            if ask_avg and bid_avg:
                acceptable_price = (ask_avg + bid_avg) / 2
            else:
            # Calculate acceptable price using most traded values.
                acceptable_price = int((gtv_ask_price + gtv_bid_price) / 2)

            pred_acc_price_20 = self.calculate_linear_regression(self.PRICE_HISTORY[product], 20, state.timestamp)
            pred_acc_price_100 = self.calculate_linear_regression(self.PRICE_HISTORY[product], 100, state.timestamp)
            print("Predicted Acceptable Price (20): ", pred_acc_price_20)
            print("Predicted Acceptable Price (100): ", pred_acc_price_100)
            self.update_price_history(product, acceptable_price, state)

            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                for price, amount in order_depth.sell_orders.items(): # Loop through each sell order.
                    if int(price) < acceptable_price: # Compare price against acceptable price to determine
                        if max_buy_volume >= amount: # Check if volume can be bought, without exceeding position limits.
                            print("BUY", str(-amount) + "x", price)
                            orders.append(Order(product, price, -amount))
                        else: # If position limit is exceeded, purchase quantity at maximum allowable volume.
                            print("BUY", str(-max_buy_volume) + "x", price)
                            orders.append(Order(product, price, -max_buy_volume))
            
            # Buy orders use same logic as sell orders.
            if len(order_depth.buy_orders) != 0:
                for price, amount in order_depth.buy_orders.items():
                    if int(price) > acceptable_price:
                        if max_sell_volume >= amount:
                            print("SELL", str(amount) + "x", price)
                            orders.append(Order(product, price, -amount))
                        else:
                            print("SELL", str(max_sell_volume) + "x", price)
                            orders.append(Order(product, price, -max_sell_volume))

            result[product] = orders

        traderData = "SAMPLE" 
        
        conversions = 1
        return result, conversions, traderData