from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        result = {'AMETHYSTS': [], 'STARFRUIT': []}

        for product in ['AMETHYST', 'STARFRUIT']:
            order_depth: OrderDepth = state.order_depths.get(product, OrderDepth())
            orders: List[Order] = []
            acceptable_price = 10;  # Participant should calculate this value
            print(f"Acceptable price for {product}: {acceptable_price}")
            print(f"Buy Order depth for {product}: {len(order_depth.buy_orders)}, Sell order depth for {product}: {len(order_depth.sell_orders)}")

            current_product_position = state.position.get(product, 0)

            print(f"CurrentPos, PosLimit for {product}: {current_product_position} {self.POSITION_LIMIT[product]}")

            if current_product_position < self.POSITION_LIMIT[product]:
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_price:
                        print(f"BUY {product}: {str(-best_ask_amount)}x at {best_ask}")
                        orders.append(Order(product, best_ask, -best_ask_amount))
                        
            if current_product_position >= self.POSITION_LIMIT[product]:
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_price:
                        print(f"SELL {product}: {str(best_bid_amount)}x at {best_bid}")
                        orders.append(Order(product, best_bid, -best_bid_amount))
    
            
            result[product] = orders
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData
