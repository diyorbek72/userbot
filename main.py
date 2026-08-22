import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import UpdateNewChannelMessage, Message
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import SendMessageRequest

# =========================
# SOZLAMALAR
# =========================
API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"
SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "ysysysysyssy"
COMMENT = "окени ами?"
# =========================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

group_input_peer = None
target_group_num_id = None

# Render uxlab qolmasligi uchun yengil server
async def handle_ping(reader, writer):
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
    await writer.drain()
    writer.close()

async def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    return await asyncio.start_server(handle_ping, "0.0.0.0", port)

async def main():
    global group_input_peer, target_group_num_id

    await start_web_server()
    print("Userbot ishga tushmoqda...", flush=True)
    await client.start()

    # Guruh ma'lumotlarini tayyorlab olamiz
    channel_entity = await client.get_entity(CHANNEL)
    full_channel = await client(GetFullChannelRequest(channel_entity))
    
    raw_group_id = full_channel.full_chat.linked_chat_id
    if not raw_group_id:
        print("[-] Kanalga guruh ulanmagan!", flush=True)
        return

    group_entity = await client.get_entity(raw_group_id)
    group_input_peer = await client.get_input_entity(group_entity)
    target_group_num_id = group_entity.id

    print(f"[+] RAW Tinglovchi yoqildi! Guruh ID: {target_group_num_id}", flush=True)
    print("⚡ MAKSIMAL TEZLIK: Telegram xom yangilanishlari tinglanmoqda...\n", flush=True)

    # Telethon filtrlarisiz, to'g'ridan-to'g'ri Telegram server paketini ilib olamiz
    @client.on(events.Raw(UpdateNewChannelMessage))
    async def raw_packet_sniper(update):
        msg = update.message
        
        # Faqat maqsadli guruh va post xabarlari uchun
        if isinstance(msg, Message) and getattr(msg.peer_id, 'channel_id', None) == target_group_num_id:
            if msg.fwd_from or msg.post:
                # 0.01 soniyada xabar uchadi
                try:
                    await client(SendMessageRequest(
                        peer=group_input_peer,
                        message=COMMENT,
                        reply_to_msg_id=msg.id,
                        random_id=int.from_bytes(os.urandom(8), 'big', signed=True)
                    ))
                    print(f"[🔥 BIRINCHI] Post #{msg.id} ga RAW-komment yuborildi!", flush=True)
                except Exception as e:
                    print(f"[!] Xatolik: {e}", flush=True)

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
