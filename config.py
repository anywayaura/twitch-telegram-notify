from environs import Env
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


env = Env()
env.read_env()

DB_NAME = env.str('DB_NAME')
# TWITCH APP  (https://dev.twitch.tv/console/apps) create app here and get client_id and client_secret
TWITCH_APP_ID = env.str('TWITCH_APP_ID')
TWITCH_APP_SECRET = env.str('TWITCH_APP_SECRET')

# TELEGRAM BOT
TG_BOT_TOKEN = env.str('TG_BOT_TOKEN')
TG_BOT_ADMIN = env.int('TG_BOT_ADMIN')
TG_BOT_CHAT_ID = env.int('TG_BOT_CHAT_ID')
TG_BOT_CHAT_THREAD_ID = env.int('TG_BOT_CHAT_THREAD_ID', None)

bot = Bot(token=TG_BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

