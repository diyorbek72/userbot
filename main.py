import os
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession


# =========================
# SOZLAMALAR
# =========================

API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"

SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "aslamboi"
COMMENT = "ку-ку"


# =========================
# TELEGRAM CLIENT
# =========================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    connection_retries=None,
    retry_delay=1,
    auto_reconnect=True
)


# =========================
# RENDER WEB SERVER
# =========================

async def handle_ping(reader, writer):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
        "Userbot active"
    )

    writer.write(response.encode())
    await writer.drain()
    writer.close()

    try:
        await writer.wait_closed()
    except Exception:
        pass


async def start_web_server():
    port = int(os.environ.get("PORT", 10000))

    server = await asyncio.start_server(
        handle_ping,
        "0.0.0.0",
        port
    )

    print(
        f"[+] Web server started: {port}",
        flush=True
    )

    return server


# =========================
# MAIN
# =========================

async def main():

    # Render portni darhol ochamiz
    await start_web_server()

    print("[+] Telegram ulanmoqda...", flush=True)

    await client.start()

    # Kanal entityni startup paytida bir marta olamiz
    channel_entity = await client.get_entity(CHANNEL)

    print(
        f"[+] Kanal ulandi: {channel_entity.title}",
        flush=True
    )

    print(
        "⚡ FAST COMMENT MODE READY!",
        flush=True
    )


    # =========================
    # DIRECT CHANNEL LISTENER
    # =========================

    @client.on(events.NewMessage(chats=channel_entity))
    async def instant_comment(event):

        try:

            # Kanal postiga bevosita comment
            await client.send_message(
                entity=channel_entity,
                message=COMMENT,
                comment_to=event.id
            )

            print(
                f"[⚡ COMMENT SENT] post={event.id}",
                flush=True
            )

        except Exception as e:

            print(
                f"[!] ERROR: "
                f"{type(e).__name__}: {e}",
                flush=True
            )


    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
