import requests
from my_secrets import TELEGRAM_BOT_TOKEN, CHAT_ID


class TelegramBot:

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.bot_url = "https://api.telegram.org/bot{}/".format(self.token)
        self.chat_id = CHAT_ID

    def send_message(self, message):
        requests.get(self.bot_url + "sendMessage?text={}&chat_id={}".format(message, self.chat_id))

    def send_dict_as_message(self, dictionary):
        text = 'Останні повідомлення з телеграм каналів: '
        for key, value in dictionary.items():
            text = text + f"\n{key}: {value}\n"
        self.send_message(text)
