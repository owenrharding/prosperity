from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:

    POSITION_LIMIT = {'AMETHYST': 20, 'STARFRUIT': 20}
    
    def run(self, state: TradingState):
        result = {'AMETHYST': [], 'STARFRUIT': []}
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            current_product_position = state.position.get(product, 0)
            
            if current_product_position < self.POSITION_LIMIT[product]:
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    acceptable_price = 5  # Participant should calculate this value
                    if int(best_ask) < acceptable_price:
                        print(f"BUY {product}: {str(best_ask_amount)}x at {best_ask}")
                        orders.append(Order(product, best_ask, best_ask_amount))
    
            if current_product_position >= self.POSITION_LIMIT[product]:
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    acceptable_price = 5  # Participant should calculate this value
                    if int(best_bid) > acceptable_price:
                        print(f"SELL {product}: {str(best_bid_amount)}x at {best_bid}")
                        orders.append(Order(product, best_bid, -best_bid_amount))
                
            result[product] = orders
    
        # Update trader data if needed
        trader_data = "SAMPLE"
        
        # Assume conversions for simplicity
        conversions = 1
        
        return result, conversions, trader_data
