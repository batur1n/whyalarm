# Why Alarm? v1.1

Are you tired of manually checking lots of Telegram channels for why an alarm was triggered?

This script monitors API endpoint for air raid alerts, analyzes recent messages from Telegram channels for alert reason (UAV/missile strike) and sends those recent messages via bot into Telegram channel https://t.me/whyalarmkyiv. Currently running 24/7 on EC2 instance.

Screenshot of how channel looks like:
![image](https://github.com/batur1n/whyalarm/assets/17457639/be4d613d-ac28-4e96-81af-32ea19743b0d)

Credits to  [@Ubilling](https://github.com/nightflyza/Ubilling) team, their API is being used in this project - more info here https://wiki.ubilling.net.ua/doku.php?id=aerialalertsapi
