from config import dp, TG_BOT_ADMIN
from twitch import check_streamers
from aiogram import types, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from database import init_db, add_streamer, delete_streamer, get_streamers
import asyncio
import aioschedule


class AdminOnlyMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Check if the user is in the list of admins
        if message.from_user.id != TG_BOT_ADMIN:
            raise CancelHandler()


@dp.message_handler(commands=['add'], chat_type=types.ChatType.PRIVATE)
async def handle_add(message: types.Message):
    try:
        streamer_name = message.text.split()[1]
        await add_streamer(streamer_name)
        await message.answer(f"Streamer '{streamer_name}' added.")
    except IndexError:
        await message.answer("Please specify a streamer name.")


@dp.message_handler(commands=['del'], chat_type=types.ChatType.PRIVATE)
async def handle_delete(message: types.Message):
    try:
        streamer_name = message.text.split()[1]
        await delete_streamer(streamer_name)
        await message.answer(f"Streamer '{streamer_name}' deleted.")
    except IndexError:
        await message.answer("Please specify a streamer name.")


@dp.message_handler(commands=['list'], chat_type=types.ChatType.PRIVATE)
async def handle_list(message: types.Message):
    streamers = [streamer[0] for streamer in await get_streamers()]
    message_text = '\n'.join(streamers)
    if message_text:
        await message.answer(message_text)
    else:
        await message.answer('list is empty')


async def scheduler():
    """планировщик задач"""
    await init_db()
    await check_streamers()
    aioschedule.every(3).minutes.do(check_streamers)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    dp.middleware.setup(AdminOnlyMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
