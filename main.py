import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Import handlers
from handlers.start_handler import start

# Load tokens
TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Flask app
app = Flask(__name__)

# Telegram async application
t_app = ApplicationBuilder().token(TOKEN).build()
t_app.add_handler(CommandHandler("start", start))


@app.post("/")
def webhook():
    """Receives Telegram updates and schedules async processing."""
    data = request.get_json(silent=True)
    if not data:
        return "no_data", 200

    update = Update.de_json(data, t_app.bot)
    asyncio.get_event_loop().create_task(t_app.process_update(update))
    return "ok", 200


async def setup_webhook():
    """Set webhook only once when container starts."""
    try:
        await t_app.bot.set_webhook(WEBHOOK_URL)
        print(f"🌍 Webhook set → {WEBHOOK_URL}")
    except Exception as e:
        print("⚠️ Webhook error:", e)


def start_bot():
    """Start telegram bot async tasks in background."""
    loop = asyncio.get_event_loop()
    loop.create_task(setup_webhook())


if __name__ == "__main__":
    print("🚀 Starting FaceSort Telegram Bot...")
    start_bot()
    print("🔥 Flask server running at 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)
