import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest

# =========================
# SOZLAMALAR
# =========================
API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"
SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "ysysysysyssy"  # @ belgisisiz yozing
COMMENT = "окени ами?"
# =========================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

channel_id = None
discussion_group_id = None

# Render uxlab qolmasligi uchun veb-server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Fast Userbot is active!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()


@client.on(events.NewMessage)
async def fast_comment_handler(event):
    global discussion_group_id, channel_id

    # Faqat biz qidirayotgan komment guruhiga kelgan xabarlarni tutamiz
    if event.chat_id != discussion_group_id:
        return

    # Faqat kanaldan avtomat ko'chirilgan postlarga javob beramiz
    # (Boshqa foydalanuvchilarning oddiy xabarlariga yozmasligi uchun)
    if event.is_channel and (event.fwd_from or event.from_id):
        try:
            # Hech qanday qo'shimcha so'rovsiz darhol REPLY yuboramiz (Millisekundlarda!)
            await event.reply(COMMENT)
            print(f"[⚡ TEZKOR] Komment birinchi bo'lib yuborildi! Post ID: {event.id}")
        except Exception as e:
            print(f"[!] Xatolik: {e}")


async def main():
    global discussion_group_id, channel_id
    print("Userbot ishga tushmoqda...")
    await client.start()

    # Kanal va uning ulangan guruhini oldindan xotiraga yuklab olamiz
    try:
        channel_entity = await client.get_entity(CHANNEL)
        channel_id = channel_entity.id

        full_channel = await client(GetFullChannelRequest(channel_entity))
        discussion_group_id = full_channel.full_chat.linked_chat_id

        if not discussion_group_id:
            print("[-] XATOLIK: Bu kanalga hech qanday komment guruhi ulanmagan!")
            return

        # ID formatini to'g'rilash (-100...)
        if not str(discussion_group_id).startswith("-100"):
            discussion_group_id = int(f"-100{discussion_group_id}")

        print(f"[+] Kanal ID: {channel_id}")
        print(f"[+] Komment guruhi ID: {discussion_group_id}")
        print("🚀 SNAYPER REJIMI YONDI: Yangi post chiqishi bilan birinchi bo'lib yoziladi!\n")

    except Exception as e:
        print(f"[!] Kanal ma'lumotlarini olishda xatolik: {e}")
        return

    await client.run_until_disconnected()


if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    client.loop.run_until_complete(main())
