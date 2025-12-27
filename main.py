import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start_handler import start

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Create a SINGLE GLOBAL event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Flask App
app = Flask(__name__)

# Telegram App
t_app = ApplicationBuilder().token(TOKEN).build()
t_app.add_handler(CommandHandler("start", start))


@app.post("/")
def webhook():
    """Telegram sends POST here → schedule async handler on global loop"""
    data = request.get_json(silent=True)
    if not data:
        return "no data", 200

    update = Update.de_json(data, t_app.bot)
    loop.create_task(t_app.process_update(update))
    return "ok", 200


async def init_webhook():
    try:
        await t_app.bot.set_webhook(WEBHOOK_URL)
        print(f"🌍 Webhook configured: {WEBHOOK_URL}")
    except Exception as e:
        print("⚠️ Webhook setup error:", e)


def start_background_loop():
    """Runs async loop forever in a parallel thread"""
    import threading
    def run():
        loop.run_forever()
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


if __name__ == "__main__":
    print("🚀 Boot: FaceSort Telegram Bot initializing")
    start_background_loop()
    loop.create_task(init_webhook())
    print("🔥 Flask is now accepting Telegram webhook updates...")
    app.run(host="0.0.0.0", port=8080)
