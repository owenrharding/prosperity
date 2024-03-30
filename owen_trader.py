from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

		# Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            
            # Position limit
            current_position = state.position.get(product, 0)
            
            # Determine max volume that can be bought/sold
            max_buy_volume = self.POSITION_LIMIT[product] - current_position
            max_sell_volume = self.POSITION_LIMIT[product] + current_position

            # Determine average ask price across orders and their corresponding amounts
            if len(order_depth.sell_orders) != 0:
                ask_sum = 0
                ask_vol = 0
                for i in range(len(order_depth.sell_orders)):
                    ask, ask_amount = list(order_depth.sell_orders.items())[i]
                    ask_sum += int(ask) * int(ask_amount)
                    ask_vol += int(ask_amount)
                ask_avg = ask_sum / ask_vol if ask_vol != 0 else 0
            else:
                ask_avg = 0
            
            # Determine average bid price across orders and their corresponding amounts
            if len(order_depth.buy_orders) != 0:
                bid_sum = 0
                bid_vol = 0
                for i in range(len(order_depth.buy_orders)):
                    bid, bid_amount = list(order_depth.buy_orders.items())[i]
                    bid_sum += int(bid) * int(bid_amount)
                    bid_vol += int(bid_amount)
                bid_avg = bid_sum / bid_vol if bid_vol != 0 else 0
            else:
                bid_avg = 0

            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]

            # Determine acceptable price by finding the mean of the best ask and bid
            if ask_avg and bid_avg:
                acceptable_price = (ask_avg + bid_avg) / 2
            else:
                acceptable_price = (best_ask + best_bid) / 2

            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            # Place buy order if market sell orders are of acceptable price
            if len(order_depth.sell_orders) != 0:
                if int(best_ask) < acceptable_price:
                    if max_buy_volume > 0: #If the current position for this product allows for more volume to be bought, then buy
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        if best_ask_amount > max_buy_volume:
                            orders.append(Order(product, best_ask, -best_ask_amount))
                        else:
                            orders.append(Order(product, best_ask, -max_buy_volume))
    
            # Place sell order if market buy orders are of acceptable price
            if len(order_depth.buy_orders) != 0:
                if int(best_bid) > acceptable_price:
                    if max_sell_volume > 0: #If the current position for this product allows for more volume to be sold, then sell
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        if best_bid_amount > max_sell_volume:
                            orders.append(Order(product, best_bid, -best_bid_amount))
                        else:
                            orders.append(Order(product, best_bid, -max_sell_volume))
            
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData