import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

API_ID = 12203269
API_HASH = os.environ["API_HASH"]

DISCUSSION_ID = -1004470296857
COMMENT = "🔥 Zo'r post!"

client = TelegramClient(
    "userbot",
    API_ID,
    API_HASH,
    connection_retries=None,
    retry_delay=1
)

processed = set()


@client.on(events.NewMessage(chats=DISCUSSION_ID))
async def handler(event):
    message = event.message

    if message.reply_to is not None:
        return

    if message.action:
        return

    if message.id in processed:
        return

    processed.add(message.id)

    try:
        await client.send_message(
            DISCUSSION_ID,
            COMMENT,
            reply_to=message.id
        )

        print(f"[+] COMMENT SENT: {message.id}")

    except FloodWaitError as e:
        print(f"[!] FloodWait: {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        print(f"[!] ERROR: {e}")


async def main():
    print("Starting...")

    await client.start()

    me = await client.get_me()

    print(f"Logged in: @{me.username or me.first_name}")
    print(f"Discussion: {DISCUSSION_ID}")
    print("Listening...")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
