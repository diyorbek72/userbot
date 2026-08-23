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

CHANNEL = "aslamboi"  # Kanal username
COMMENT = "шошип поймела"
# =========================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Render uchun server
async def handle_ping(reader, writer):
    # Brauzer uchun chiroyliroq javob
    html = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    html += "<html><body style='background:black; color:lime; text-align:center; padding-top:20%; font-family:sans-serif;'>"
    html += "<h1>🚀 Userbot 24/7 Aktiv!</h1>"
    html += "<p>Hammasi joyida, bot yangi postlarni kutyapti...</p>"
    html += "</body></html>"
    
    writer.write(html.encode())
    await writer.drain()
    writer.close()

async def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    return await asyncio.start_server(handle_ping, "0.0.0.0", port)

async def main():
    await start_web_server()
    print("Userbot ishga tushmoqda...", flush=True)
    await client.start()

    try:
        # Kanal va uning komment guruhini xotiraga olish
        channel_entity = await client.get_entity(CHANNEL)
        target_channel_id = channel_entity.id

        full_channel = await client(GetFullChannelRequest(channel_entity))
        raw_group_id = full_channel.full_chat.linked_chat_id
        
        if not raw_group_id:
            print("[-] XATO: Kanalga hech qanday komment guruhi ulanmagan!", flush=True)
            return

        group_entity = await client.get_entity(raw_group_id)
        print(f"[+] Ulandi! Kanal ID: {target_channel_id} | Guruh ID: {group_entity.id}", flush=True)
        print("⚡ SNAYPER TAYYOR: Faqat kanaldan kelgan postlarga yozadi!\n", flush=True)

        # Guruhni tinglash
        @client.on(events.NewMessage(chats=group_entity))
        async def fast_commenter(event):
            is_target_channel_post = False

            # 1. Telegram kanaldan avtomat ko'chirgan post bo'lsa
            if event.fwd_from:
                fwd_channel_id = getattr(event.fwd_from.from_id, 'channel_id', None)
                if fwd_channel_id == target_channel_id or event.fwd_from.channel_post:
                    is_target_channel_post = True

            # 2. Xabar to'g'ridan-to'g'ri kanal nomidan chiqsa
            sender_channel_id = getattr(event.from_id, 'channel_id', None)
            if sender_channel_id == target_channel_id:
                is_target_channel_post = True

            # Agar oddiy odam yozgan bo'lsa, o'tkazib yuboramiz
            if not is_target_channel_post:
                return

            # Faqat maqsadli postga tezkor reply yuborish
            try:
                await client.send_message(
                    entity=group_entity,
                    message=COMMENT,
                    reply_to=event.id
                )
                print(f"[🔥 BIRINCHI] Kanal posti #{event.id} ga komment yozildi!", flush=True)
            except Exception as e:
                print(f"[!] Xatolik: {e}", flush=True)

    except Exception as e:
        print(f"[!] Sozlashda xatolik: {e}", flush=True)
        return

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
