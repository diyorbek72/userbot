import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest

# =========================
# SOZLAMALAR
# =========================
API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"
SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "aslamboi"
COMMENT = "sinatr sila"

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
    server = await asyncio.start_server(handle_ping, "0.0.0.0", port)
    print(f"[+] Web server started: {port}", flush=True)
    return server

# =========================
# MAIN
# =========================
async def main():
    await start_web_server()
    print("[+] Telegram ulanmoqda...", flush=True)
    await client.start()

    try:
        # Kanal va guruhni oldindan bir marta aniqlab keshlaymiz
        channel_entity = await client.get_entity(CHANNEL)
        target_channel_id = channel_entity.id

        full_channel = await client(GetFullChannelRequest(channel_entity))
        raw_group_id = full_channel.full_chat.linked_chat_id

        if not raw_group_id:
            print("[-] XATO: Kanalga hech qanday komment guruhi ulanmagan!", flush=True)
            return

        group_entity = await client.get_entity(raw_group_id)
        print(f"[+] Kanal: {channel_entity.title} | Guruh ID: {group_entity.id}", flush=True)
        print("⚡ ULTRA-FAST SNIPER READY!", flush=True)

        # To'g'ridan-to'g'ri guruhni tinglaymiz (Eng tezkor yo'l)
        @client.on(events.NewMessage(chats=group_entity))
        async def instant_comment(event):
            # Faqat maqsadli kanaldan kelgan yangi post ekanligini tekshirish
            is_channel_post = False

            if event.fwd_from:
                fwd_id = getattr(event.fwd_from.from_id, 'channel_id', None)
                if fwd_id == target_channel_id or event.fwd_from.channel_post:
                    is_channel_post = True

            sender_id = getattr(event.from_id, 'channel_id', None)
            if sender_id == target_channel_id:
                is_channel_post = True

            if not is_channel_post:
                return

            try:
                # 0.2 soniyada bitta so'rov bilan yuborish
                await client.send_message(
                    entity=group_entity,
                    message=COMMENT,
                    reply_to=event.id
                )
                print(f"[⚡ COMMENT SENT] post={event.id}", flush=True)
            except Exception as e:
                print(f"[!] ERROR: {type(e).__name__}: {e}", flush=True)

    except Exception as e:
        print(f"[!] Sozlashda xatolik: {e}", flush=True)
        return

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
