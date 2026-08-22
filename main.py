import os
import base64
import asyncio

from telethon import TelegramClient, events
from telethon.errors import FloodWaitError


# =========================
# TELEGRAM
# =========================

API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"

DISCUSSION_ID = -1004470296857

COMMENT = "окени ами?"


# =========================
# RESTORE SESSION
# =========================

session_b64 = os.environ["SESSION_B64"]

with open("userbot.session", "wb") as f:
    f.write(base64.b64decode(session_b64))

print("[+] Session restored")


# =========================
# CLIENT
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
# NEW DISCUSSION MESSAGE
# =========================

@client.on(events.NewMessage(chats=DISCUSSION_ID))
async def handler(event):

    message = event.message

    # Reply/commentlarni o'tkazib yuboramiz
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

        print(
            f"[!] FloodWait: "
            f"{e.seconds}s"
        )

        await asyncio.sleep(e.seconds)

    except Exception as e:

        print(
            f"[!] ERROR: "
            f"{type(e).__name__}: {e}"
        )


# =========================
# MAIN
# =========================

async def main():

    print("Starting userbot...")

    await client.connect()

    if not await client.is_user_authorized():

        print(
            "[!] ERROR: "
            "Session is not authorized!"
        )

        return

    me = await client.get_me()

    print("--------------------------------")
    print("Telegram Auto Comment Userbot")
    print("--------------------------------")

    print(
        f"Account: "
        f"@{me.username or me.first_name}"
    )

    print(
        f"Discussion: "
        f"{DISCUSSION_ID}"
    )

    print(
        f"Comment: "
        f"{COMMENT}"
    )

    print("Listening...")
    print("--------------------------------")

    await client.run_until_disconnected()


if __name__ == "__main__":

    asyncio.run(main())
