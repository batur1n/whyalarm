"""
1. Listen for webhook and wait for air alert to commence
2. Once webhook is triggered, scan telegram channels for information
3. Telegram bot sends aggregated message to own channel, with alert time and reason(s)
"""

from bs4 import BeautifulSoup
import requests

CHANNELS = {
    "https://t.me/s/kpszsu": "ПС ЗСУ", 
    "https://t.me/s/vanek_nikolaev": "Ванек", 
    "https://t.me/s/war_monitor": "Монітор"
    }

def get_last_messages(channels: dict) -> list(str):
    """Collect latest messages from telegram channels"""
    result = []

    for channel_url, channel_name in channels.items():
        channel = requests.get(channel_url, timeout=10).text
        soup = BeautifulSoup(channel, 'lxml')
        last_message = soup.find_all('div', class_ = 'tgme_widget_message_text')[-1].text
        result.append(channel_name, last_message)

    return result
