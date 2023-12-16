"""
1. Listen for webhook and wait for air alert to commence
2. Once webhook is triggered, scan telegram channels for information
3. Telegram bot sends aggregated message to own channel, with alert time and reason(s)
"""

from bs4 import BeautifulSoup
import requests
from my_secrets import TELEGRAM_CHANNELS


def get_last_messages():
    """Collect latest messages from telegram channels"""

    result = {}

    for channel_url, channel_name in TELEGRAM_CHANNELS.items():
        channel = requests.get(channel_url, timeout=10).text
        soup = BeautifulSoup(channel, 'lxml')
        last_message = soup.find_all('div', class_ ='tgme_widget_message')[-1]
        last_message_text = last_message.find('div', class_ = 'tgme_widget_message_text').text
        last_message_timestamp = last_message.find('time', class_ = 'time').get('datetime')
        result[channel_name] = [last_message_timestamp, last_message_text]

    return result
