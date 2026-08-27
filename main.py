import os
import time
import random
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions import PingRequest

API_ID = 22894500
API_HASH = "5e1b0f96c7b351e22d4c868d3389aa30"
SESSION_STRING = os.environ.get("SESSION_STRING", "1ApWapzMBuzPujKcJ5A7TTioCee8tOuggp9j5oRGIr4hPDjM5hb2I_NgV7nkaEJgrifeQWSkPKvpowWdW50pHNB85UL6x-p3a__1d-tcht8m3O-mYHyalNShS11O_HbdcLlC10kv-Hp4dLoENpD-BZ98Agm2JvV0VXKkcxbFZTDy4WzSi-8LYb2brAe2S_Bn3w2erQx-7QPutV3btZkMqST8KW_oPfQDzXDjr0kXBAKiZNF77wBT9A6E3w6XHd5vqYLAm7Pyq5w7ZAi7WuvRGTpvy0fSf4kPLgfsuCHpl9lqgWYv1TJ-Y8BsNZDrwBS97LqhQDS638wfKbBcqBdx_8rlu6UHg5gA=")

CHANNEL = "aslamboi"

COMMENTS = [
    "sinatr sila?",
    "okeni ami?",
    "Xm",
    "Hm",
    "Salon",
    "reak bos yban",
    "Aken budjet?"
]

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    connection_retries=None,
    auto_reconnect=True
)

group_entity = None
target_channel_id = None

async def socket_keep_alive():
    while True:
        await asyncio.sleep(30)
        try:
            await client(PingRequest(ping_id=random.randint(0, 999999)))
        except Exception:
            pass

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.ping$"))
async def ping_benchmark(event):
    start = time.perf_counter()
    msg = await event.edit("⚡")
    end = time.perf_counter()
    ms = round((end - start) * 1000, 2)
    
    await msg.edit(
        f"⚡Chat ping: {ms} ms\n"
        f"👤 Developer: Zro (Railway C-Core)\n"
        f"📍 Server: Railway (Yevropa)\n"
        f" stealth: Ultra-Snayper Aktiv 🎯"
    )

async def instant_dot_and_edit(msg_id):
    try:
        sent_msg = await client.send_message(
            entity=group_entity,
            message=".",
            reply_to=msg_id
        )
        print(f"[🔥 1-O'RIN BAND QILINDI] Msg #{msg_id} ga nuqta ketdi!", flush=True)

        chosen_comment = random.choice(COMMENTS)
        await sent_msg.edit(chosen_comment)
        print(f"[✏️ TAHRIRLANDI] -> '{chosen_comment}'", flush=True)
    except Exception as e:
        print(f"[!] Xatolik: {e}", flush=True)

async def main():
    global group_entity, target_channel_id
    print("[+] Telegram ulanmoqda...", flush=True)
    await client.start()

    channel_entity = await client.get_entity(CHANNEL)
    target_channel_id = channel_entity.id

    full_channel = await client(GetFullChannelRequest(channel_entity))
    raw_group_id = full_channel.full_chat.linked_chat_id
    group_entity = await client.get_entity(raw_group_id)

    print(f"[+] KANAL ID: {target_channel_id} | GURUH ID: {group_entity.id}", flush=True)
    print("⚡ RAILWAY HARDCORE SNAYPER ISHGA TUSHDI!\n", flush=True)

    asyncio.create_task(socket_keep_alive())

    @client.on(events.NewMessage(chats=group_entity))
    async def ultra_fast_listener(event):
        if event.fwd_from:
            fwd_id = getattr(event.fwd_from.from_id, 'channel_id', None)
            if fwd_id == target_channel_id or event.fwd_from.channel_post:
                asyncio.create_task(instant_dot_and_edit(event.id))
                return

        if getattr(event.from_id, 'channel_id', None) == target_channel_id:
            asyncio.create_task(instant_dot_and_edit(event.id))

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
