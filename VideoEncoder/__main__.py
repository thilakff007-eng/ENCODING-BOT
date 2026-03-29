import dns.resolver
from pyrogram import idle
from flask import Flask
import threading
import os
import asyncio

from . import app, log

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']


# 🔹 Your bot main function
def start_bot():
    import time
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())  # ✅ direct call
        except Exception as e:
            print("Bot crashed:", e)
            time.sleep(5)


# 🔹 Flask app (for Render)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Encoding Bot Running ✅"


# 🔹 Run bot in background
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


threading.Thread(target=start_bot).start()


# 🔹 Run Flask (Render needs this)
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=PORT)
