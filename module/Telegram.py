import telegram
import requests
import config

TAG = "Telegram"

class Telegram:
    def __init__(self):
        self.chat_id = config.CHAT_ID
        self.token = config.TOKEN
        self.bot = telegram.Bot(token = self.token)

    def send_message(self, message):
        requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}")

telegram = Telegram()