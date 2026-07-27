import asyncio

# Python 3.12+ versiyalarda event loop xatosini tuzatish
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
from datetime import datetime
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# 2023-yil 8-martdan hisoblaydi
START_DATE = datetime(2023, 3, 8, 0, 0, 0)

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)


def calculate_time():
    now = datetime.now()
    diff = now - START_DATE

    days = diff.days
    total_seconds = diff.seconds

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return (
        f"❤️ **2023-yil 8-martdan beri birga:**\n\n"
        f"🗓 **{days}** kun\n"
        f"⏰ **{hours}** soat\n"
        f"⏱ **{minutes}** daqiqa\n"
        f"⚡️ **{seconds}** soniya"
    )


@app.on_message(filters.me & filters.text & filters.regex("^¥$"))
async def start_counter(client, message):
    try:
        while True:
            await message.edit_text(calculate_time())
            await asyncio.sleep(3)
    except Exception as e:
        print(f"Xatolik: {e}")


app.run()
