"""
Main script which runs 24/7 on EC2 instance and listens for alarms.
In case of an alarm, it sends a message to a channel using telegram bot.
There is also scraping/parsing part to notify users why alarm was triggered.
"""
from telegram.tg_channels import TelegramChannels
from telegram.tg_bot import TelegramBot
from utils import Utils
from my_secrets import ALERTS_API_ENDPOINT


def main():
    """Main function with infinite loop to run on server"""
    utils = Utils()
    telegram_bot = TelegramBot()
    telegram_channels = TelegramChannels()
    info_posted = False

    while True:
        alert_info = utils.get_alert_info(ALERTS_API_ENDPOINT)
        if alert_info['alertnow'] and not info_posted:
            telegram_bot.send_message("У Києві оголошено повітряну тривогу! Деталі через 30сек-2хв")
            messages = telegram_channels.get_messages_near_timestamp(alert_info['changed'])
            reason = telegram_channels.parse_messages_for_alert_reason(messages)
            utils.get_map_image(ALERTS_API_ENDPOINT)
            telegram_bot.send_photo(caption=reason)
            telegram_bot.send_dict_as_message(messages)
            info_posted = True
        elif not alert_info['alertnow'] and info_posted:
            telegram_bot.send_message('Відбій повітряної тривоги.')
            info_posted = False
        utils.wait(6)

if __name__ == '__main__':
    main()
