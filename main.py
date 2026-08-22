import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# =========================
# SOZLAMALAR
# =========================
API_ID = 12203269
API_HASH = "5bfb8b0e68d86a267afe2ebe87fb2335"
# Renderdagi Environment Variable orqali o'qiydi
SESSION_STRING = os.environ.get("SESSION_STRING")

CHANNEL = "@ysysysysyssy"
COMMENT = "окени ами?"
# =========================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNEL))
async def new_post(event):
    if not event.is_channel:
        return

    message = event.message
    if not message.replies:
        print(f"[-] Post #{message.id}: discussion yo'q")
        return

    print(f"[+] Yangi post: {message.id}")
    try:
        discussion = await client(
            __import__("telethon").functions.messages.GetDiscussionMessageRequest(
                peer=CHANNEL,
                msg_id=message.id
            )
        )
        if not discussion.messages:
            return

        discussion_message = discussion.messages[0]
        discussion_chat = discussion.chats[0]

        await client.send_message(
            discussion_chat,
            COMMENT,
            reply_to=discussion_message.id
        )
        print(f"[+] COMMENT YUBORILDI | post={message.id}")

    except FloodWaitError as e:
        print(f"[!] FloodWait: {e.seconds}s kutamiz")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"[!] Xatolik: {e}")

# Render o'chib qolmasligi uchun soxta port ochish
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Userbot 24/7 ishlayapti!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

async def main():
    print("Userbot ishga tushmoqda...")
    await client.start()
    me = await client.get_me()
    print(f"Ulandi: @{me.username or me.first_name}")
    print("Kanal postlari kutilmoqda...\n")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    client.loop.run_until_complete(main())
