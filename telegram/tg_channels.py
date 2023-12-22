"""This module contains stuff which works with telegram channels"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
import requests
from my_secrets import TELEGRAM_CHANNELS
from utils import Utils


class TelegramChannels:
    """Class for scraping and parsing messages from telegram channels on web"""

    def __init__(self):
        self.telegram_channels = TELEGRAM_CHANNELS
        self.keywords = {'UAV': ["shahed", "шахед", "шахид", "мопед", "бпла", "безпілотник"],
                         'MISSILE': ["пуск", "ракет", "баліст", "баллист", "авіа", "х-"],
                         'PLANE': ["миг", "міг"]}

    def scrape_last_messages(self, timestamp):
        """Collect latest messages from telegram channels"""
        result = {}
        for channel_url, channel_name in self.telegram_channels.items():
            channel_page = requests.get(channel_url, timeout=30).text
            soup = BeautifulSoup(channel_page, 'lxml')
            messages = soup.find_all('div', class_ ='tgme_widget_message')
            for message in messages:
                message_timestamp = datetime.fromisoformat(message.find('time', class_ = 'time').get('datetime'))
                if timestamp+timedelta(minutes=10) >= message_timestamp >= timestamp-timedelta(minutes=10):
                    result[channel_name] = message.find('div', class_ = 'tgme_widget_message_text').text
                    break
        return result

    def get_messages_near_timestamp(self, alert_timestamp):
        """Filter messages based on timestamp. Returns messages which were 
        posted right after or 10 minutes before the alarm was triggered"""
        alert_datetime = datetime.fromisoformat(alert_timestamp)
        while True:
            Utils.wait(1, "Getting last messages from Telegram channels on web")
            last_messages = self.scrape_last_messages(alert_datetime.astimezone(ZoneInfo("Europe/Kyiv")))
            if any(value for value in last_messages.values()):
                return last_messages
            Utils.wait(29, "Nothing found, waiting for new messages")

    def parse_messages_for_alert_reason(self, messages_dict):
        """Parse messages and see if keywords are in text"""
        for _, message in messages_dict.items():
            for keyword in self.keywords['PLANE']:
                if keyword in message.lower():
                    return '✈️ Зліт МіГ-31К'
            for keyword in self.keywords['UAV']:
                if keyword in message.lower():
                    return '💣 Загроза ударних дронів'
            for keyword in self.keywords['MISSILE']:
                if keyword in message.lower():
                    return '🚀 Загроза ракетного удару'
        return None
