from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    products = {
        'AMETHYSTS': {'Position_Limit': 20, 'Current_Position': 0},
        'STARFRUIT': {'Position_Limit': 20, 'Current_Position': 0}
    }
        
    def run(self, state: TradingState):
        conversions = 0

        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        result = {}

        for product_name, product_info in self.products.items():
            order_depth: OrderDepth = state.order_depths.get(product_name, OrderDepth())
            orders: List[Order] = []
            acceptable_price = 10;  # Participant should calculate this value
            print(f"Acceptable price for {product_name}: {acceptable_price}")
            print(f"Buy Order depth for {product_name}: {len(order_depth.buy_orders)}, Sell order depth for {product_name}: {len(order_depth.sell_orders)}")
            current_product_position = state.position.get(product_name, 0)

            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]

            if len(order_depth.sell_orders) != 0:
                for i in range(len(order_depth.sell_orders)-1):
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[i]
                    best_ask_2, best_ask_amount_2 = list(order_depth.sell_orders.items())[i+1]
                    if best_ask_amount_2 > best_ask_amount:
                        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[i+1]

            if len(order_depth.buy_orders) != 0:
                for i in range(len(order_depth.buy_orders) - 1):
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[i]
                    best_bid_2, best_bid_amount_2 = list(order_depth.buy_orders.items())[i+1]
                    if best_bid_amount_2 > best_bid_amount:
                        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[i+1] 

            acceptable_price_price = int((best_ask + best_bid) / 2)

            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product_name, best_ask, -best_ask_amount))

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product_name, best_bid, -best_bid_amount))

            #if current_product_position < product_info['Position_Limit']:
            #if len(order_depth.sell_orders) != 0:
            #    best_ask = float('inf')
            #    best_ask_amount = 0
            #    for ask, amount in order_depth.sell_orders.items():
            #        if int(ask) < best_ask and int(ask) < acceptable_price:
            #            best_ask = int(ask)
            #            best_ask_amount = amount
                
            #    if best_ask != float('inf'):
            #        print(f"BUY {product_name}: {str(-best_ask_amount)}x at {best_ask}")
            #        orders.append(Order(product_name, best_ask, -best_ask_amount))
                        
            #if current_product_position >= product_info['Position_Limit']:
            #if len(order_depth.buy_orders) != 0:
            #    best_bid = float('-inf')
            #    best_bid_amount = 0
            #    for bid, amount in order_depth.buy_orders.items():
            #        if int(bid) > best_bid and int(bid) > acceptable_price:
            #            best_bid = int(bid)
            #            best_bid_amount = amount

            #    if best_bid != float('-inf'):
            #        print(f"SELL {product_name}: {str(best_bid_amount)}x at {best_bid}")
            #        orders.append(Order(product_name, best_bid, -best_bid_amount))    
            
            result[product_name] = orders
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData
