"""
TradingState class: Holds all information that algorithm needs to make decisions about which orders to send.

own_trades: Dictionary of Trades the algorithm has done since the last TradingState came in.
market_trades: Dictionary of Trades the other market participants have done since the last TradingState came in.
position: Dictionary of long or short position that we hold in every tradable product.
order_depths: Dictionary of all the buy and sell orders per product that other market participants have sent and the algorithm is able to trade with. 
"""
Time = int
Symbol = str
Product = str
Position = int

class TradingState(object):

    def __init__(self,
                 traderData: str,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 own_trades: Dict[Symbol, List[Trade]],
                 market_trades: Dict[Symbol, List[Trade]],
                 position: Dict[Product, Position],
                 observations: Observation):
        self.traderData = traderData
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


"""
Trade class: A transaction of a product.

symbol: Product that the trade corresponds to.
price: The price that product was exchanged.
quantity: The quantity that was exchanged.
buyer: The identity of the buyer in the transaction.
seller: The identity of the seller in the transaction.
"""
Symbol = str
UserId = str

class Trade:

    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = None, seller: UserId = None, timestamp: int = 0) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"


"""
OrderDepth class: Collection of all outstanding buy and sell orders for a particular product.

In both of these dictionaries, the keys are the price and the values are the total volume on that price level.
E.g. If buy_orders was {9: 5, 10: 4}, that means there is a total buy order quantity at price level 9, and a total buy order quantity of 4 at price level 10.
"""
class OrderDepth:

    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}


"""
Observation class: 

In TradingState, two observation items are given. #Note: can only see one instance of observation in TradingState? #
One is a simple product to value dictionary inside plainValueObservations.
The other is a dictionary of complex ConversionObservation values for respective products. Used to place conversion requests from Trader class. Structure visible below.
"""
class ConversionObservation:

    def __init__(self, bidPrice: float, askPrice: float, transportFees: float, exportTariff: float, importTariff: float, sunlight: float, humidity: float):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.transportFees = transportFees
        self.exportTariff = exportTariff
        self.importTariff = importTariff
        self.sunlight = sunlight
        self.humidity = humidity


"""
Order: Proposed order for a product placed by the run() function in Trader class.

I think the difference between an Order and a Trade is that an Order is proposed but may not be accepted, while a Trade is a confirmed Order?
"""
Symbol = str

class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"