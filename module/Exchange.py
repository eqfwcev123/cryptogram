import ccxt
import config

class Exchange:
    def __init__(self):
        self.exchange = ccxt.bitget({
            "apiKey": config.API_KEY,
            "secret": config.SECRET_KEY,
            "password": config.PASSWORD
        })
        self.markets = self.exchange.load_markets()
        self.symbols = [] # [{"ticker":"BTC/USDT:USDT", "timeframe":"5m"}]
        self.limit = 1000

        try:
            balance = self.exchange.fetch_balance()

            print("Connected to Bitget API")
        except:
            print("Failed to connect to Bitget account. Please check your API Key and secret key")

    # ohlcv => open, high , low, close, volume
    def get_latest_ohlcvs(self):
        latest_ohlcvs = []
        for symbol in self.symbols:
            latest_ohlcv = self.exchange.fetch_ohlcv(
                symbol["ticker"],
                symbol["timeframe"],
                limit = 1
            )[0]
            latest_ohlcvs.append(latest_ohlcv)
        
        return latest_ohlcvs
    
    def get_history_ohlcvs(self, index):
        return self.exchange.fetch_ohlcv(
            self.symbols[index]["ticker"],
            self.symbols[index]["timeframe"],
            limit = self.limit
            )

    def add_symbols(self, new_symbols):
        """
        @new_symbol: [{"ticker": "Valid ticker", "timeframe": "Valid timeframe"}]
        """
        for new_symbol in new_symbols:
            if len(self.symbols) > 0:
                for symbol in self.symbols:
                    if new_symbol["ticker"] not in symbol["ticker"]:
                        self.symbols.append(new_symbol)
            else:
                self.symbols.append(new_symbol)

    def set_limit(self, limit):
        self.limit = limit


exchange = Exchange()