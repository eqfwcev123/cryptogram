import ccxt
from module.Telegram import telegram
import talib
import numpy as np
import requests
import time

from datetime import datetime
from module.Strategy import strategy as Strategy
from module.Exchange import exchange as Exchange

Exchange.add_symbols(
    [{
        "ticker": "BTC/USDT:USDT",
        "timeframe": "5m",
    },
    {
        "ticker": "ETH/USDT:USDT",
        "timeframe": "5m",
    },
    {
        "ticker": "XRP/USDT:USDT",
        "timeframe": "5m",
    }]
)
latest_timestamps = np.zeros_like(Exchange.symbols)


while True:
    # Fetch latest dataset
    latest_ohlcvs = Exchange.get_latest_ohlcvs()

    for index, latest_ohlcv in enumerate(latest_ohlcvs):
        ohlcv_timestamp = latest_ohlcv[0]
        ohlcv_open = latest_ohlcv[1]
        ohlcv_high = latest_ohlcv[2]
        ohlcv_low = latest_ohlcv[3]
        ohlcv_close = latest_ohlcv[4]

        # Check if the latest timestamp is already in the data
        if ohlcv_timestamp > latest_timestamps[index]:
            latest_timestamps[index] = ohlcv_timestamp

        # Fetch full dataset
        ohlcv_data = Exchange.get_history_ohlcvs(index)
        history_data_close_prices = np.array([ohlcv[4] for  ohlcv in ohlcv_data])

        Strategy.EMA25Strategy(
            ohlcv_close, 
            history_data_close_prices, 
            Exchange.symbols[index]["timeframe"],
            Exchange.symbols[index]["ticker"]
            )

    time.sleep(1)

