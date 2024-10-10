from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor


TG_BOT_TOKEN = '01234567890:abcdefghijklmnopqrstuvwxyz' # <- WRITE YOUR TG_BOT_TOKEN HERE


bot = Bot(token=TG_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(content_types='text')
async def echo(message: types.Message):
    TG_CHAT_ID = message.chat.id
    TG_CHAT_THREAD_ID = message.message_thread_id if hasattr(message, 'message_thread_id') else None
    TG_BOT_ADMIN = message.from_user.id

    print(f"Message: {message.text}, TG_CHAT_ID: {TG_CHAT_ID}, TG_CHAT_THREAD_ID: {TG_CHAT_THREAD_ID}, SENDER_ID: {TG_BOT_ADMIN}")

    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
