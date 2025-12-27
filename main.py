import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start_handler import start
from utils.db import users

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN missing")
    raise SystemExit(1)

if not WEBHOOK_URL:
    print("❌ ERROR: WEBHOOK_URL missing")
    raise SystemExit(1)

print("🚀 Starting FaceSort Telegram Bot...")

# Build bot
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# REQUIRED to enable webhook processing
asyncio.run(bot_app.initialize())

app = Flask(__name__)

@app.post("/")
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot_app.bot)
        asyncio.run(bot_app.process_update(update))
    except Exception as e:
        print("⚠️ Webhook error:", e)
    return "ok", 200


if __name__ == "__main__":
    try:
        print("🌍 Setting Telegram webhook:", WEBHOOK_URL)
        asyncio.run(bot_app.bot.set_webhook(url=WEBHOOK_URL))
    except Exception as e:
        print("⚠️ Webhook set error:", e)

    print("🔥 Flask server running 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)
