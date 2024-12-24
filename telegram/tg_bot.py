"""Module for working with telegram bot"""
import sys
import os.path
import requests
from my_secrets import TELEGRAM_BOT_TOKEN, CHAT_ID


class TelegramBot:
    """Class which contains telegram bot methods"""

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.bot_url = f"https://api.telegram.org/bot{self.token}/"
        self.chat_id = CHAT_ID

    def send_message(self, message):
        """Simple method to send any string message"""
        requests.get(self.bot_url+f'sendMessage?text={message}&chat_id={self.chat_id}', timeout=10)

    def send_dict_as_message(self, dictionary):
        """Method to send dict in a pretty printed format"""
        text = 'Останні повідомлення з телеграм каналів: \n'
        for key, value in dictionary.items():
            text = text + f"\n{key}: {value}\n"
        self.send_message(text)
        sys.stdout.write("\nAlert reasons posted on telegram channel!")

    def send_photo(self, caption):
        """Method to send photo with caption"""
        params = {'chat_id': self.chat_id, 'caption': caption}
        file = open(os.path.join(os.path.dirname(__file__), '..', 'map.png'), 'rb')
        requests.post(self.bot_url+'sendPhoto', params, files={'photo': file}, timeout=30)
        file.close()
