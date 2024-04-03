from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}

    PROD_STATE_COUNT = {'AMETHYSTS': 0, 'STARFRUIT': 0}

    BUY_FLAGS = {'AMETHYSTS': False, 'STARFRUIT': False}
    SELL_FLAGS = {'AMETHYSTS': False, 'STARFRUIT': False}

    # Best Acceptable Prices (BAP) with varying scopes
    BAP_GLOBAL = {'AMETHYSTS': 0, 'STARFRUIT': 0} # Best Acceptable Price ever recorded for the product
    BAP_1 = {'AMETHYSTS': 0, 'STARFRUIT': 0} 
    BAP_2 = {'AMETHYSTS': 0, 'STARFRUIT': 0} 

    # Historical Acceptable Prices (HAP) with varying numbers of value reserves
    HAP_1 = {'AMETHYSTS': [], 'STARFRUIT': []}
    HAP_2 = {'AMETHYSTS': [], 'STARFRUIT': []}

    BAP_LIST = [BAP_1, BAP_2]
    BAP_SCOPE = {'BAP_1': 20, 'BAP_2': 100}
    HAP_LIST = [HAP_1, HAP_2]
    HAP_SCOPE = {'HAP_1': 20, 'HAP_2': 100}
    
    def calculate_baps_and_haps(self, product: str, current_acceptable_price: int):
        # Set Historical Acceptable Price (HAP) values based off acceptable price for current Trading State:
        for hap in self.HAP_LIST:
            # Initially populate HAP
            if len(self.haps) < self.HAP_SCOPE[hap]:
                self.hap[product].append(current_acceptable_price)
            else:
                # Remove first value from self.HAP_1[product], THEN ###############################################################################
                self.hap[product].append(current_acceptable_price)
        
        # Calculate Best Acceptable Price (BAP) values based off acceptable price for current Trading State:
        # Global
        if current_acceptable_price > self.BAP_GLOBAL[product]:
            self.BAP_GLOBAL[product] = current_acceptable_price
        # Scoped
        for bap in self.BAP_LIST:
            bap_counter = 0
            corresponding_hap = self.HAP_LIST[bap_counter][product]
            self.bap = avg(corresponding_hap)

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
                ###################acceptable_price = (best_ask + best_bid) / 2######################################################################
                acceptable_price = None

            self.calculate_baps_and_haps(product, acceptable_price)

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
                        if -best_bid_amount > max_sell_volume:
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