from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from math import *
import string

"""
Trader class: coding logic contained in here.

Single method run(), which is called every time a new TradingState is available.
Should return a dictionary name result which contains all the orders the algorithm in run() decides to send.
"""
class Trader:

    def run(self, state: TradingState):
        # Result should be a dictionary of all the orders that the algorithm decides to spend
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10  # Participant should calculate this value
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
        return result

    def calculate_mean_reversion():
        # I'm thinking that, rather than calculating the mean of each product
        # each time we get a new TradingState, we should calculate it once, store the mean of
        # each product somewhere, and then update it when we get a new TradingState
        # However, the following is how you calculate mean reversion, super simple:


        # Get mean of product: mean = sumOfPrices/numberOfObservations
        mean = 0
        numberOfObservations = len(priceList)
        sumOfPrices = 0

        for price in priceList:
            sumOfPrices += price
        
        mean = sumOfPrices/numberOfObservations

        # Find current deviation from mean: deviation = price - mean
        deviation = priceList[-1] - mean # I think this is the syntax for the lastmost index of a list? I forgot :/

        # Find standard deviation: standardDeviation = squareRoot(sumOfSquaredDeviations/(Number of Observations - 1))
        sumOfSquaredDeviations = 0
        for price in priceList:
            priceDevSquared = (price - mean) ** 2
            sumOfSquaredDeviations += priceDevSquared
        
        meanOfSquaredDeviations = sumOfSquaredDeviations/numberOfObservations
        standardDeviation = sqrt(meanOfSquaredDeviations) # Note: this is different to how I wrote it up there ^, the way I've done it here is how I found it on MathsIsFun. Not sure if it's right but it'll do for now

        # Calculate Z-score: zScore = deviation/standardDeviation
        zScore = deviation/standardDeviation

        # Then, a Z-score above a certain threshold (commonly 1.5 or 2) may indicate the asset is overvalued, and
        # below a certain threshold (commonly -1.5 or -2) may indicate the asset is undervalued.
        

        # From here, could use different strategies such as Moving Averages, Bollinger Bands, Relative Strength Index, Stochastic Oscillator, or Moving Average Convergence Divergence
        # Mean reversion has limitations, which include the fact that it is less effective in strongly trending markets, where prices may not revert to the mean for extended periods.
        # If there's a way to calculate this, we could do some logic on a ratio of how much we take mean_reversion into account, and how much we take a different strategy into account
        pass
