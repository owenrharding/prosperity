from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    products = {
        'AMETHYSTS': {'Position_Limit': 20, 'Current_Position': 0},
        'STARFRUIT': {'Position_Limit': 20, 'Current_Position': 0}
    }
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

		# Orders to be placed on exchange matching engine
        result = {}
        for product_name, product_info in self.products.items():
            order_depth: OrderDepth = state.order_depths[product_name]
            orders: List[Order] = []
            
            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]

            if len(order_depth.sell_orders) != 0:
                for i in range(len(order_depth.sell_orders) - 1):
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

            acceptable_price = int((best_ask + best_bid) / 2)

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
            
            result[product_name] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
