import dns.resolver
from pyrogram import idle
from flask import Flask
import threading
import os
import asyncio

from . import app, log

# Fix DNS issue (important for MongoDB)
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']


# 🔹 Main bot function
async def main():
    print("BOT STARTING...")  # debug

    await app.start()

    me = await app.get_me()
    await app.send_message(
        chat_id=log,
        text=f"<b>Bot Started! @{me.username}</b>"
    )

    await idle()
    await app.stop()


# 🔹 Flask app (to keep Render alive)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Encoding Bot Running ✅"


# 🔹 Run bot in background with auto-restart
def start_bot():
    import time

    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
        except Exception as e:
            print("Bot crashed:", e)
            time.sleep(5)  # restart after crash


# Start bot thread
threading.Thread(target=start_bot, daemon=True).start()


# 🔹 Start Flask server (Render needs this)
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=PORT)
