import os
import base64
import asyncio

from aiohttp import web
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError


# =========================
# CONFIG
# =========================

API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"

DISCUSSION_ID = -1004470296857
COMMENT = "окени ами?"

PORT = int(os.environ.get("PORT", 10000))


# =========================
# RESTORE SESSION
# =========================

session_b64 = os.environ["SESSION_B64"]

with open("userbot.session", "wb") as f:
    f.write(base64.b64decode(session_b64))

print("[+] Session restored")


# =========================
# TELEGRAM CLIENT
# =========================

client = TelegramClient(
    "userbot",
    API_ID,
    API_HASH,
    connection_retries=None,
    retry_delay=1
)

processed = set()


# =========================
# TELEGRAM EVENT
# =========================

@client.on(events.NewMessage(chats=DISCUSSION_ID))
async def handler(event):

    message = event.message

    # Faqat root message
    if message.reply_to is not None:
        return

    # Service message
    if message.action:
        return

    # Duplicate
    if message.id in processed:
        return

    processed.add(message.id)

    try:
        await client.send_message(
            DISCUSSION_ID,
            COMMENT,
            reply_to=message.id
        )

        print(
            f"[+] COMMENT SENT | "
            f"message={message.id}"
        )

    except FloodWaitError as e:
        print(f"[!] FloodWait: {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        print(
            f"[!] ERROR: "
            f"{type(e).__name__}: {e}"
        )


# =========================
# WEB SERVER
# =========================

async def health(request):
    return web.Response(text="OK")


async def start_web_server():
    app = web.Application()

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        PORT
    )

    await site.start()

    print(f"[+] Web server started on port {PORT}")


# =========================
# TELEGRAM
# =========================

async def start_telegram():

    print("[+] Starting Telegram...")

    await client.connect()

    if not await client.is_user_authorized():
        print("[!] ERROR: Session is not authorized!")
        return

    me = await client.get_me()

    print("--------------------------------")
    print("Telegram Auto Comment Userbot")
    print("--------------------------------")
    print(
        f"Account: "
        f"@{me.username or me.first_name}"
    )
    print(f"Discussion: {DISCUSSION_ID}")
    print(f"Comment: {COMMENT}")
    print("Listening...")
    print("--------------------------------")

    await client.run_until_disconnected()


# =========================
# MAIN
# =========================

async def main():

    # MUHIM:
    # Avval portni ochamiz.
    # Telegram connection undan keyin boshlanadi.

    await start_web_server()

    telegram_task = asyncio.create_task(
        start_telegram()
    )

    await telegram_task


if __name__ == "__main__":
    asyncio.run(main())
