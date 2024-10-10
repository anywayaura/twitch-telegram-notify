import aiosqlite
from config import DB_NAME, TG_BOT_CHAT_ID, bot


# Async SQLite database setup (run once at startup)
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS streamers (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                message_id INTEGER
            )
        ''')
        await db.commit()


# Async function to add a streamer
async def add_streamer(name):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute('INSERT INTO streamers (name) VALUES (?)', (name,))
            await db.commit()
        except aiosqlite.IntegrityError:
            pass  # Streamer already exists, ignore


# Async function to delete a streamer
async def delete_streamer(name):
    async with aiosqlite.connect(DB_NAME) as db:
        # Fetch the message_id for the streamer
        cursor = await db.execute('SELECT message_id FROM streamers WHERE name = ?', (name,))
        row = await cursor.fetchone()

        if row and row[0]:  # If message_id is not None or NULL
            message_id = row[0]
            try:
                await bot.delete_message(TG_BOT_CHAT_ID, message_id)
            except Exception as e:
                print(f"Error deleting message {message_id}: {e}")

        # Now delete the streamer from the database
        await db.execute('DELETE FROM streamers WHERE name = ?', (name,))
        await db.commit()


# Async function to get all streamers
async def get_streamers():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT name, message_id FROM streamers') as cursor:
            streamers = await cursor.fetchall()
    return streamers


# Async function to set message_id for a streamer
async def set_message_id(name, message_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE streamers SET message_id = ? WHERE name = ?', (message_id, name))
        await db.commit()
