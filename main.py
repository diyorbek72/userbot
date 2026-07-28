import asyncio

# Python 3.12+ event loop fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
from datetime import datetime
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# Render portini ushlash uchun veb-server
web_app = Flask("")


@web_app.route("/")
def home():
    return "Userbot va Avto-Kommentariya 24/7 ishlamoqda!"


def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()


# USERBOT KODI
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# ============================================================
# AVTO-KOMMENTARIYA SOZLAMALARI:
TARGET_CHANNEL = "diorvs99"  # Sizning kanalingiz
TARGET_GROUP = "hshsuahabaja"  # Sizning muhokama guruhingiz
COMMENT_TEXT = "Birinchi! ❤️"  # Avtomatik yoziladigan matn
# ============================================================

START_DATE = datetime(2023, 3, 8, 0, 0, 0)

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)


# 1. TAYMER FUNKSIYASI (¥)
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
            try:
                await message.edit_text(calculate_time())
                await asyncio.sleep(1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Xatolik: {e}")


# 2. AVTO-KOMMENTARIYA FUNKSIYASI (Guruhda avto-postga instant reply)
@app.on_message(filters.chat(TARGET_GROUP) | filters.chat(f"@{TARGET_GROUP}"))
async def auto_comment_in_group(client, message):
    try:
        # Kanaldan guruhga tushgan post bo'lsa
        if (
            message.is_automatic_forward
            or message.forward_from_chat
            or message.sender_chat
        ):
            await message.reply_text(COMMENT_TEXT)
            print(
                f"MUVAFFAQIYATLI: [{message.id}] postga guruhda komment yozildi!"
            )
    except Exception as e:
        print(f"Guruhda komment xatosi: {e}")


keep_alive()
print("Userbot va Avto-Kommentariya ishga tushdi!")
app.run()
