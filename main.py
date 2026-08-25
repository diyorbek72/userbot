import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetDiscussionMessageRequest

# =========================
# SOZLAMALAR
# =========================
API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"
SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "aslamboi"  # Kanal username
COMMENT = "sinatr sila"  # Kommentingiz
# =========================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    connection_retries=None,
    retry_delay=1,
    auto_reconnect=True
)

# Render uchun server
async def handle_ping(reader, writer):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
        "Direct Channel Sniper Active"
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
    return await asyncio.start_server(handle_ping, "0.0.0.0", port)

async def main():
    await start_web_server()
    print("[+] Telegram ulanmoqda...", flush=True)
    await client.start()

    # Kanal ob'ektini oldindan tayyorlab olamiz
    channel_entity = await client.get_entity(CHANNEL)
    print(f"[+] KANAL TO'G'RIDAN-TO'G'RI NISHONDA: {channel_entity.title}", flush=True)
    print("🚀 GURUHNI KUTMASDAN, 0.00-SONIYADAYOQ ZARBA BERILADI!\n", flush=True)

    # GURUHNI EMAS, KANALNING O'ZINI TINGLAYMIZ!
    @client.on(events.NewMessage(chats=channel_entity))
    async def direct_channel_sniper(event):
        try:
            # 1. Post chiqishi bilan uning discussion manzilini olamiz (~10ms)
            discussion = await client(GetDiscussionMessageRequest(
                peer=channel_entity,
                msg_id=event.id
            ))
            
            if discussion and discussion.messages:
                # 2. Hech qanday kechikishsiz darhol komment jo'natamiz (~15ms)
                await client.send_message(
                    entity=discussion.chats[0],
                    message=COMMENT,
                    reply_to=discussion.messages[0].id
                )
                print(f"[🔥 1-O'RIN] Post #{event.id} ga 0.03 soniyada komment ketdi!", flush=True)

        except Exception as e:
            print(f"[!] Xatolik: {e}", flush=True)

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
