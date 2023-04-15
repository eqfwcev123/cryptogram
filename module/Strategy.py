import talib
import numpy as np
from module.Telegram import telegram as Telegram

# 정배열/역배열 확인 필요
class Strategy:
    # TODO: Have to add condition to filter out sideway market
    def EMA25Strategy(self, current_price, close_prices, timeframe, symbol):
        ema_25 = talib.EMA(close_prices, timeperiod=25)[-1]
        ema_50 = talib.EMA(close_prices, timeperiod=50)[-1]
        ema_100 = talib.EMA(close_prices, timeperiod=100)[-1]

        high = max([ema_25, ema_50, ema_100])
        low = min([ema_25, ema_50, ema_100])

        if high == ema_25 and low == ema_100:
            # Currently in Bullish EMA Crossover
            if current_price >= ema_25:
                message = f'[Bullish EMA] Current market price ({current_price}) is touching the 25 EMA ({ema_25}) on the {timeframe} chart for {symbol}'
                Telegram.send_message(message)
        else:
            # Currently in Bearish EMA Crossover
            if current_price <= ema_25:
                message = f'[Bearish EMA] Current market price ({current_price}) is touching the 25 EMA ({ema_25}) on the {timeframe} chart for {symbol}'
                Telegram.send_message(message)
        
        
strategy = Strategy()
    