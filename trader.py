from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}

    def calc_order(self, product: str, order_depth: OrderDepth, current_position: int):
        product_orders: List[Order] = []

        # Initialise best ask and bid to null
        best_ask = None
        best_bid = None

        # Extract the best ask from order_depth, where best sell order is the lowest priced sell order on the market
        if order_depth.sell_items:
            best_ask = min(order_depth.sell_orders.keys())

        # Extract the best bid from order depth, where best buy order is the highest priced buy order on the market
        if order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())

        # Determine max volume that can be bought/sold based on current position 
        max_buy_volume = self.POSITION_LIMIT[product] - current_position 
        max_sell_volume = current_position - self.POSITION_LIMIT[[product]]

        # Add calculated order to product order
        ### BUY ### 
        if best_ask is not None:
            product_orders.append(Order(product, best_ask, max_buy_volume))

        ### SELL ###
        if best_bid is not None:
            product_orders.append(Order(product, best_bid, max_sell_volume))

        return product_orders

    def run(self, state: TradingState):

        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {'AMETHYSTS': [], 'STARFRUIT': []}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            current_position = state.position[product]
            
            orders: List[Order] = self.calc_order(product, order_depth, current_position)
            
            result[product] = orders
    
        return result