from datamodel import OrderDepth, UserId, TradingState, Order
import collections
from collections import defaultdict
from typing import List
import string
import copy

empty_dict = {'AMETHYSTS' : 0, 'STARFRUIT' : 0}

class Trader:

    POSITION_LIMIT = {'AMETHYSTS': 20, 'STARFRUIT': 20}
    position = copy.deepcopy(empty_dict)
    cpnl = defaultdict(lambda : 0)
    volume_traded = copy.deepcopy(empty_dict)

    def values_extract(self, order_dict, buy=0):
        tot_vol = 0
        best_val = -1
        mxvol = -1

        for ask, vol in order_dict.items():
            if(buy==0):
                vol *= -1
            tot_vol += vol
            if tot_vol > mxvol:
                mxvol = vol
                best_val = ask
        
        return tot_vol, best_val
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        result = {'AMETHYSTS': [], 'STARFRUIT': []}

        for product in ['AMETHYSTS', 'STARFRUIT']:
            order_depth: OrderDepth = state.order_depths.get(product, OrderDepth())
            orders: List[Order] = []
            acceptable_price = 10;  # Participant should calculate this value
            print(f"Acceptable price for {product}: {acceptable_price}")
            print(f"Buy Order depth for {product}: {len(order_depth.buy_orders)}, Sell order depth for {product}: {len(order_depth.sell_orders)}")

            current_product_position = state.position.get(product, 0)
            print(f"CurrentPos, PosLimit for {product}: {current_product_position} {self.POSITION_LIMIT[product]}")

            osell = collections.OrderedDict(sorted(order_depth.sell_orders.items()))
            obuy = collections.OrderedDict(sorted(order_depth.buy_orders.items(), reverse=True))

            sell_vol, best_sell_pr = self.values_extract(osell)
            buy_vol, best_buy_pr = self.values_extract(obuy, 1)
            
            undercut_buy = best_buy_pr + 1
            undercut_sell = best_sell_pr - 1

            lb = 10000
            ub = 10000

            acc_bid = {'AMETHYSTS' : lb, 'STARFRUIT' : lb} # we want to buy at slightly below
            acc_ask = {'AMETHYSTS' : ub, 'STARFRUIT' : ub} # we want to sell at slightly above

            bid_pr = min(undercut_buy, acc_bid-1) # we will shift this by 1 to beat this price
            sell_pr = max(undercut_sell, acc_ask+1)

            current_pos = self.position[product]

            if (current_pos < self.POSITION_LIMIT[product]) and (self.position[product] < 0):
                newnum = min(40, self.POSITION_LIMIT[product] - current_pos)
                orders.append(Order(product, min(undercut_buy - 1, acc_bid - 1), newnum))
                current_pos += newnum
                             
            if (current_pos < self.POSITION_LIMIT[product]) and (self.position[product] > 15):
                newnum = min(40, self.POSITION_LIMIT[product] - current_pos)
                orders.append(Order(product, min(undercut_buy - 1, acc_bid - 1), newnum))
                current_pos += newnum

            if (current_pos < self.POSITION_LIMIT[product]):
                newnum = min(40, self.POSITION_LIMIT[product] - current_pos)
                orders.append(Order(product, bid_pr, newnum))
                current_pos += newnum

            result[product] += orders
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
