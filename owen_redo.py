from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    # Define position limits for each product.
    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20, 'ORCHIDS': 100}

    # Define price history dictionaries for each product. These will store every historical acceptable price calculated by the algorithm.
    # These are stored in dictionaries, where timestamp is the key, and the acceptable price is the value.
    PRICE_HISTORY = {'AMETHYSTS': {}, 'STARFRUIT': {}, 'ORCHIDS': {}}

    ORCHID_PRODUCTION_RATE = 0

    """
    Updates price history arrays stored in Trader class.
    """
    def update_price_history(self, product: str, new_data_point: float, state: TradingState):
        # Add acceptable price to corresponding product in PRICE_HISTORY dictionary
        if product in self.PRICE_HISTORY:
            self.PRICE_HISTORY[product][state.timestamp] = new_data_point

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

            # Get values with greatest trading volume (GTV).
            gtv_ask_price = list(order_depth.sell_orders.items())[-1][0]
            gtv_bid_price = list(order_depth.buy_orders.items())[-1][0]
            
            # Calculate acceptable price using most traded values.
            acceptable_price = int((gtv_ask_price + gtv_bid_price) / 2)

            # Update historical data with newly calculated acceptable price
            self.update_price_history(product, acceptable_price, state)

            if product == 'ORCHIDS':
                sunlight = state.observations.conversionObservations[product].sunlight
                humidity = state.observations.conversionObservations[product].humidity
                print("SUNLIGHT:", state.observations.conversionObservations[product].sunlight)
                print("HUMIDITY:", state.observations.conversionObservations[product].humidity)


            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            #if len(order_depth.sell_orders) != 0:
            #    for price, amount in order_depth.sell_orders.items(): # Loop through each sell order.
            #        if int(price) < acceptable_price: # Compare price against acceptable price to determine
            #            if max_buy_volume >= amount: # Check if volume can be bought, without exceeding position limits.
            #                print("BUY", str(-amount) + "x", price)
            #                orders.append(Order(product, price, -amount))
            #            else: # If position limit is exceeded, purchase quantity at maximum allowable volume.
            #                print("BUY", str(-max_buy_volume) + "x", price)
            #                orders.append(Order(product, price, -max_buy_volume))
            
            ## Buy orders use same logic as sell orders.
            #if len(order_depth.buy_orders) != 0:
            #    for price, amount in order_depth.buy_orders.items():
            #        if int(price) > acceptable_price:
            #            if max_sell_volume >= amount:
            #                print("SELL", str(amount) + "x", price)
            #                orders.append(Order(product, price, -amount))
            #            else:
            #                print("SELL", str(max_sell_volume) + "x", price)
            #                orders.append(Order(product, price, -max_sell_volume))

            result[product] = orders

        traderData = "SAMPLE" 
        
        conversions = 1
        return result, conversions, traderData