"""
Main script which runs 24/7 on EC2 instance and listens for alarms.
In case of an alarm, it sends a message to a channel using telegram bot.
There is also scraping/pasing part to notify users why alarm was triggered
"""
import sys
from datetime import datetime

from telegram.tg_channels import TelegramChannels
from telegram.tg_bot import TelegramBot
from utils import Utils
from my_secrets import ALERTS_API_ENDPOINT


def main():
    """Main function with infinite loop"""
    info_posted = False
    utils = Utils()
    telegram_bot = TelegramBot()
    telegram_channels = TelegramChannels()
    while True:
        kyiv_info = utils.get_alert_info(ALERTS_API_ENDPOINT)
        if kyiv_info['alertnow'] and not info_posted:
            telegram_bot.send_message("У Києві оголошено повітряну тривогу! Деталі через 30сек-2хв")
            alert_timestamp = datetime.fromisoformat(kyiv_info['changed'])
            utils.wait(30, "Waiting 30 seconds for Telegram channels to post some info")
            messages = telegram_channels.get_messages_near_timestamp(alert_timestamp)
            telegram_bot.send_dict_as_message(messages)
            sys.stdout.write("\nAlert reasons posted on telegram channel!")
            info_posted = True
        elif not kyiv_info['alertnow'] and info_posted:
            telegram_bot.send_message('Відбій повітряної тривоги.')
            info_posted = False
        utils.wait(6)

if __name__ == '__main__':
    main()
