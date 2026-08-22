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

CHANNEL = "ysysysysyssy"  # Kanal username
COMMENT = "окени ами?"
# =========================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Render uchun server
async def handle_ping(reader, writer):
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
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
        full_channel = await client(GetFullChannelRequest(channel_entity))
        
        raw_group_id = full_channel.full_chat.linked_chat_id
        if not raw_group_id:
            print("[-] XATO: Kanalga hech qanday komment guruhi ulanmagan!", flush=True)
            return

        group_entity = await client.get_entity(raw_group_id)
        print(f"[+] Guruh ulandi! Guruh ID: {group_entity.id}", flush=True)
        print("⚡ SNAYPER TAYYOR: Yangi post chiqishi bilan xatoliksiz komment yozadi!\n", flush=True)

        # To'g'ridan-to'g'ri komment guruhini tinglash
        @client.on(events.NewMessage(chats=group_entity))
        async def fast_commenter(event):
            # Kanaldan avtomat ko'chirilgan post yoki kanal nomidan chiqqan xabarni aniqlash
            if event.fwd_from or event.is_channel or event.sender_id == channel_entity.id:
                try:
                    # Telethon 1.44 uchun eng tezkor va xatosiz reply
                    await client.send_message(
                        entity=group_entity,
                        message=COMMENT,
                        reply_to=event.id
                    )
                    print(f"[🔥 BIRINCHI] Post #{event.id} ga komment yuborildi!", flush=True)
                except Exception as e:
                    print(f"[!] Xatolik: {e}", flush=True)

    except Exception as e:
        print(f"[!] Sozlashda xatolik: {e}", flush=True)
        return

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
