import os
import random
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import SendMessageRequest

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

group_input_peer = None
target_group_id = None

# Render uxlab qolmasligi uchun
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Ultra-Fast Sniper Active")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

async def main():
    global group_input_peer, target_group_id

    print("Userbot ishga tushmoqda...")
    await client.start()

    # Kanal va Guruhni oldindan to'liq xotiraga yuklab "InputPeer" tayyorlaymiz
    channel_entity = await client.get_entity(CHANNEL)
    full_channel = await client(GetFullChannelRequest(channel_entity))
    
    raw_group_id = full_channel.full_chat.linked_chat_id
    if not raw_group_id:
        print("[-] Kanalga guruh ulanmagan!")
        return

    # Guruhning to'liq ob'ektini va InputPeer manzilini olamiz
    group_entity = await client.get_entity(raw_group_id)
    group_input_peer = await client.get_input_entity(group_entity)
    target_group_id = group_entity.id

    print(f"[+] To'g'ridan-to'g'ri Guruh nishonga olindi! Guruh ID: {target_group_id}")
    print("⚡ SNAYPER TAYYOR: Millisekundlarda javob beradi!\n")

    # To'g'ridan-to'g'ri faqat shu guruhni tinglaymiz
    @client.on(events.NewMessage(chats=group_entity))
    async def ultra_fast_handler(event):
        # Guruhga tushgan post kanaldan kelganini tekshirish
        if event.fwd_from or event.is_channel:
            # Hech qanday keraksiz tekshiruvlarsiz TO'G'RIDAN-TO'G'RI RAW SO'ROV YUBORAMIZ:
            try:
                await client(SendMessageRequest(
                    peer=group_input_peer,
                    message=COMMENT,
                    reply_to_msg_id=event.id,
                    random_id=random.randint(0, 9223372036854775807)
                ))
                print(f"[🔥 1-O'RIN] Post #{event.id} ga soniya ulushida komment ketdi!")
            except Exception as e:
                print(f"[!] Xatolik: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    client.loop.run_until_complete(main())
