import aiohttp  # Async HTTP client
from config import TWITCH_APP_ID, TWITCH_APP_SECRET
from config import bot, TG_BOT_CHAT_ID, TG_BOT_CHAT_THREAD_ID
from database import get_streamers, set_message_id
from aiogram.utils.exceptions import BadRequest, MessageNotModified, MessageCantBeDeleted, MessageCantBeEdited, MessageToEditNotFound
from aiogram.utils.markdown import hbold, hitalic
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



async def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                print(f"Response: {await response.json()}")
            response.raise_for_status()
            return (await response.json())['access_token']


async def is_stream_live(streamer_name, client_id, oauth_token):
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    url = 'https://api.twitch.tv/helix/streams'
    params = {
        'user_login': streamer_name
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = (await response.json())['data']
            if data:
                return True, data[0]  # Stream is live
            return False, None  # Stream is not live


async def check(streamer_name, oauth_token):
    live, stream_data = await is_stream_live(streamer_name, TWITCH_APP_ID, oauth_token)

    if live:
        message_text = hbold(f'{streamer_name} стримит {stream_data["game_name"]}!') + hitalic(f'\n{stream_data["title"].replace("#", "")}\n')
    else:
        message_text = None
    return message_text


async def check_streamers():
    oauth_token = await get_oauth_token(TWITCH_APP_ID, TWITCH_APP_SECRET)

    streamers = {name: message_id for name, message_id in await get_streamers()}
    for streamer, existing_message in streamers.items():

        message_text = await check(streamer, oauth_token)
        keyboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='смотреть', url=f'https://twitch.tv/{streamer}'))

        if message_text and not existing_message:
            try:
                message = await bot.send_message(TG_BOT_CHAT_ID, text=message_text, message_thread_id=TG_BOT_CHAT_THREAD_ID, reply_markup=keyboard)
                await set_message_id(streamer, message.message_id)
            except BadRequest:
                if 'thread not found' in str(e):
                    message = await bot.send_message(TG_BOT_CHAT_ID, text=message_text, reply_markup=keyboard)
                    await set_message_id(streamer, message.message_id)
                else:
                    print(f'Error while sending message {e}')

        elif message_text and existing_message:
            try:
                await bot.edit_message_text(message_text, TG_BOT_CHAT_ID, existing_message, reply_markup=keyboard)
            except MessageNotModified:
                pass
            except (MessageCantBeEdited, MessageToEditNotFound):
                try:
                    message = await bot.send_message(TG_BOT_CHAT_ID, text=message_text, message_thread_id=TG_BOT_CHAT_THREAD_ID, reply_markup=keyboard)
                    await set_message_id(streamer, message.message_id)
                except BadRequest as e:
                    if 'thread not found' in str(e):
                        message = await bot.send_message(TG_BOT_CHAT_ID, text=message_text, reply_markup=keyboard)
                        await set_message_id(streamer, message.message_id)
                    else:
                        print(f'Error while sending message {e}')
            except Exception as ex:
                print(f'Error while editing message: {ex}')


        elif not message_text and existing_message:
            try:
                await bot.delete_message(TG_BOT_CHAT_ID, existing_message)
            except MessageCantBeDeleted:
                pass
            finally:
                await set_message_id(streamer, None)
