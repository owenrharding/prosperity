from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    products = {
        'AMETHYSTS': {'Position_Limit': 20, 'Current_Position': 0},
        'STARFRUIT': {'Position_Limit': 20, 'Current_Position': 0}
    }
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {'AMETHYST': [], 'STARFRUIT': []}

        for product_name, product_info in self.products.items():
            order_depth: OrderDepth = state.order_depths[product_name]
            orders: List[Order] = []

            acceptable_price = 5  # Participant should calculate this value  

            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            currentPos = product_info['Current_Position']

            if currentPos < product_info['Position_Limit']: # Buy
                maxBuyQty = product_info['Position_Limit'] - product_info['Current_Position']
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = max(order_depth.sell_orders.items(), key=lambda x: x[0])
                    if int(best_ask) < acceptable_price:
                        print("BUY"), str(-best_ask_amount) + "x", best_ask)
                        num = max(-40, -product_info['Position_Limit'] -product_info['Current_Position'])
                        orders.append(Order(product_name, best_ask, maxBuyQty))
                        product_info["Current_Position"] += num

            if currentPos >= product_info['Position_Limit']: # Sell
                maxSellQty = product_info['Position_Limit'] - product_info['Current_Position']

                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = max(order_depth.buy_orders.items(), key=lambda x: x[0])
                    if int(best_bid) > acceptable_price:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        num = min(40, product_info['Position_Limit'] - product_info['Current_Position'])
                        orders.append(Order(product_name, best_bid, maxSellQty))
                        product_info["Current_Position"] += num

            result[product_name] = orders    
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData
