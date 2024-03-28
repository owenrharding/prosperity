from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    POSITION_LIMIT = {'AMETHYST': 20, 'STARFUIT': 20}

    def determine_acceptable_price(state: TradingState):
        pass
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {'AMETHYST': [], 'STARFRUIT': []}

        # Iterate over all the keys (the available products) contained in the order dephts
        for key, val in state.position.items():
            self.position[key] = val
        print()
        for key, val in state.position.items():
            print(f'{key} position: {val}')

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            acceptable_price = 5  # Participant should calculate this value

            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            currentProductPosition = state.position[product]

            ### BUY ### 
            # If current position is less than the position limit, then it's okay to buy
            if currentProductPosition < self.POSITION_LIMIT[product]:
                # Buying the max buy quantity would place our position at the upper position limit
                maxBuyQty = self.POSITION_LIMIT[product] - currentProductPosition

                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_price:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, maxBuyQty))
    
            ### SELL ###
            # If current position is greater than or equal to the position limit, then it's okay to sell
            if currentProductPosition >= self.POSITION_LIMIT[product]:
                # Selling the max sell quantity would place our position at the lower position limit
                maxSellQty = currentProductPosition - self.POSITION_LIMIT[product]

                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_price:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, maxSellQty))
            
            result[product] = orders
    
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData