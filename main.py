import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start_handler import start
from utils.db import users

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not TOKEN:
    print("❌ BOT_TOKEN missing!")
    raise SystemExit(1)

if not WEBHOOK_URL:
    print("❌ WEBHOOK_URL missing!")
    raise SystemExit(1)

print("🚀 Starting bot...")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

bot_app.add_handler(CommandHandler("start", start))

@app.post("/")
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        bot_app.process_update(update)
    except Exception as e:
        print("⚠️ webhook error:", e)
    return "ok"

# Railway needs THIS to keep container alive
if __name__ == "__main__":
    print("🌍 Setting webhook:", WEBHOOK_URL)
    import asyncio
    asyncio.run(bot_app.bot.set_webhook(url=WEBHOOK_URL))

    print("🔥 Flask server running @ 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)
