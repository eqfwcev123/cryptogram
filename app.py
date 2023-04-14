import ccxt
import telegram
import talib
import numpy as np
import requests
import time
import config

from datetime import datetime

token = config.TOKEN
chat_id = config.CHAT_ID
bot = telegram.Bot(token=token)

exchange = ccxt.bitget({
    "apiKey": config.API_KEY,
    "secret": config.SECRET_KEY,
    "password": config.PASSWORD
})

balance = exchange.fetch_balance()

if len(balance['total']) == 0:
    print('Failed to fetch balance. Please check your API key and secret key.')
else:
    print("Connected to Bitget")

symbol = "ETH/USDT"
timeframe = "5m"
limit=1000
latest_timestamp = 0

# ohlcv => open, high , low, close, volume

while True:
    # Fetch latest dataset
    latest_ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1)
    # timestamp = datetime.fromtimestamp(latest_ohlcv[0][0]/1000)
    latest_ohlcv_timestamp = latest_ohlcv[0][0]

    # Check if the latest timestamp is already in the data
    if latest_ohlcv_timestamp > latest_timestamp:
        latest_timestamp = latest_ohlcv_timestamp

        # Fetch full dataset
        ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

        # Calculate the 25 EMA, 50 EMA, and 100 EMA
        close_prices = np.array([ohlcv[4] for ohlcv in ohlcv_data])
        ema_25 = talib.EMA(close_prices, timeperiod=25)[-1]
        ema_50 = talib.EMA(close_prices, timeperiod=50)[-1]
        ema_100 = talib.EMA(close_prices, timeperiod=100)[-1]

        # Check if current market price is touching 25 EMA
        current_price = latest_ohlcv[0][4]
        if current_price >= ema_25:
            # Send a signal using Telegram
            message = f'Current market price ({current_price}) is touching the 25 EMA ({ema_25}) on the {timeframe} chart for {symbol}'
            requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}')
        else:
            requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text="Test"')

    time.sleep(1)

