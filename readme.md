# twitch-telegram-notify
Simple async bot sending a notification to target chat if streamer is live on twitch, updating notification message info, and deleting message when the streamer is offline. Supports multiple streamers.


### install requirements
```
pip install -r requirements.txt
```

### credentials
1) create app here [dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps), get TWITCH_APP_ID, TWITCH_APP_SECRET
2) create telegram bot at [@botfather](https://t.me/BotFather), get TG_BOT_TOKEN and write it in echo.py
3) add bot as admin to needed group/channel
3) use telegram echo bot to get:
    - TG_BOT_CHAT_ID, (where to send notifications)
    - TG_BOT_CHAT_THREAD_ID (topic_id if you using topics in the group, if not)
    - TG_BOT_ADMIN (sender_id)
    1) run `python echo.py`
    2) send test message to target group/channel/private_message,
    3) read values in echo bot:
        >Message: asadkjhfj, TG_CHAT_ID: -9876543210, TG_CHAT_THREAD_ID: None, SENDER_ID: 0123456789

### create .env file
fill it with your credentials, example:
```
DB_NAME = streamers.db
TWITCH_APP_ID = 'abcdefghijklmnopqrstuvwxyz'
TWITCH_APP_SECRET = 'abcdefghijklmnopqrstuvwxyz'
TG_BOT_TOKEN = '01234567890:abcdefghijklmnopqrstuvwxyz'
TG_BOT_CHAT_ID = -012345567890
TG_BOT_ADMIN = 0123456789
```

### run bot
```
python bot.py
```

### bot commands
manage streams u want to be notified about with these commands:
- `/add <streamer_name>`
- `/del <streamer_name>`
- `/list`
