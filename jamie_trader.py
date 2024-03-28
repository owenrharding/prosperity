from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    POSITION_LIMIT = {'AMETHYST': 20, 'STARFRUIT': 20}
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        result = {'AMETHYST': [], 'STARFRUIT': []}
        for product in state.order_depths:
            acceptable_price = 5
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            currentProductPosition = state.position.get(product, 0)
            
            if currentProductPosition < self.POSITION_LIMIT[product]:
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_price:
                        print(f"BUY {product}: {str(-best_ask_amount)}x at {best_ask}")
                        orders.append(Order(product, best_ask, -best_ask_amount))
    
            if currentProductPosition >= self.POSITION_LIMIT[product]:
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_price:
                        print(f"SELL {product}: {str(best_bid_amount)}x at {best_bid}")
                        orders.append(Order(product, best_bid, -best_bid_amount))
                
            result[product] = orders
    
        # Update trader data if needed
        traderData = "SAMPLE"
        
        # Assume conversions for simplicity
        conversions = 1
        timestamp = 0
       
        return result, conversions, traderData, timestamp
