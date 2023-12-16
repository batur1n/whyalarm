import sys
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests

from tg_channels import get_last_messages
from tg_bot import TelegramBot

ALERTS_URL = 'https://ubilling.net.ua/aerialalerts/'

def get_kyiv_info():
    """Get alert info for Kyiv area"""
    sys.stdout.write("\nSending GET request to alerts API... ")
    response = requests.get(ALERTS_URL, timeout=10)
    if response.status_code != 200:
        sys.stdout.write(f"\nGET request failed: {response.status_code}, {response.reason}")
    else:
        sys.stdout.write(f'{response.status_code} OK')
        return response.json()['states']['м. Київ']

def wait(seconds, message="Waiting for updates"):
    """Display dots in stdout while waiting"""
    sys.stdout.write('\n'+message)
    for _ in range(seconds*2):
        time.sleep(.5)
        sys.stdout.write('.')
        sys.stdout.flush()

def find_telegram_info(alert_timestamp, timeout=30):
    results = {}
    alert_timestamp_tz = alert_timestamp.astimezone(ZoneInfo("Europe/Kyiv"))

    while not results:
        wait(timeout, f"Waiting {timeout} seconds for Telegram channels to post some info")
        last_messages = get_last_messages()
        sys.stdout.write("\nGetting last messages from Telegram channels on web...")
        for channel, message in last_messages.items():
            if (datetime.fromisoformat(message[0]) > alert_timestamp_tz) or \
               (datetime.fromisoformat(message[0]) < alert_timestamp_tz-timedelta(minutes=10)):
                results[channel] = message[1]

    return results

def main():
    info_posted = False
    telegram_bot = TelegramBot()
    while True:
        kyiv_info = get_kyiv_info()
        if kyiv_info['alertnow'] and not info_posted:
            telegram_bot.send_message("У Києві оголошено повітряну тривогу! Деталі через декілька хвилин.")
            alert_timestamp = datetime.fromisoformat(kyiv_info['changed'])
            telegram_bot.send_dict_as_message(find_telegram_info(alert_timestamp))
            info_posted = True
        elif not kyiv_info['alertnow'] and info_posted:
            info_posted = False
        wait(3)
                    
if __name__ == '__main__':
    main()
