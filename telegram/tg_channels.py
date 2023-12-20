"""This module contains stuff whcih works with telegram channels"""
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
import requests
from my_secrets import TELEGRAM_CHANNELS


class TelegramChannels:
    """Class for scraping and parsing messages from telegram channels on web"""

    def __init__(self):
        self.telegram_channels = TELEGRAM_CHANNELS
        self.keywords = {'UAV': ["шахід", "шахед", "шахид", "мопед", "бпла", "безпілотник"],
                         'MISSILE': ["пуск", "ракет", "баліст", "баллист", "авіа", "х-"]}

    def scrape_last_messages(self):
        """Collect latest messages from telegram channels"""
        result = {}
        for channel_url, channel_name in self.telegram_channels.items():
            channel = requests.get(channel_url, timeout=10).text
            soup = BeautifulSoup(channel, 'lxml')
            last_message = soup.find_all('div', class_ ='tgme_widget_message')[-1]
            last_message_text = last_message.find('div', class_ = 'tgme_widget_message_text').text
            last_message_timestamp = last_message.find('time', class_ = 'time').get('datetime')
            result[channel_name] = [last_message_timestamp, last_message_text]
        return result

    def get_messages_near_timestamp(self, alert_timestamp):
        """Filter messages based on timestamp. Returns messages which were 
        posted right after or 10 minutes before the alarm was triggered"""
        results = {}
        alert_datetime = datetime.fromisoformat(alert_timestamp)
        alert_timestamp_tz = alert_datetime.astimezone(ZoneInfo("Europe/Kyiv"))
        while True:
            last_messages = self.scrape_last_messages()
            sys.stdout.write("\nGetting last messages from Telegram channels on web...")
            for channel, message in last_messages.items():
                if (datetime.fromisoformat(message[0]) > alert_timestamp_tz) or \
                (datetime.fromisoformat(message[0]) > alert_timestamp_tz-timedelta(minutes=10)):
                    results[channel] = message[1]
            if any(value for value in results.values()):
                return results

    def parse_messages_for_alert_reason(self, messages_dict):
        """Parse messages and see if keywords are in text"""
        for _, message in messages_dict.items():
            for keyword in self.keywords['UAV']:
                if keyword in message.lower():
                    return '💣 Загроза ударних дронів'
            for keyword in self.keywords['MISSILE']:
                if keyword in message.lower():
                    return '🚀 Загроза ракетного удару'
        return None
