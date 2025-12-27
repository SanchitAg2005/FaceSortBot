import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

from handlers.start_handler import start  # <-- your handler

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)

# Create single global Application instance
t_app = Application.builder().token(TOKEN).build()
t_app.add_handler(CommandHandler("start", start))


# Background runner to keep bot alive
async def run_bot():
    print("🚀 Telegram Bot Async Loop started...")
    await t_app.initialize()
    await t_app.start()
    print("🌍 Setting webhook...")
    await t_app.bot.set_webhook(WEBHOOK_URL)
    await t_app.updater.start_webhook()
    await asyncio.Event().wait()  # keep running forever without exiting


@app.post("/")
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, t_app.bot)
        # Dispatch update asynchronously
        asyncio.create_task(t_app.process_update(update))
    except Exception as e:
        print("⚠️ Error in webhook:", e)

    return "ok", 200


if __name__ == "__main__":
    print("🚀 Boot: FaceSort Telegram Bot initializing")

    # Create event loop only ONCE
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    print("🔥 Flask is now accepting Telegram webhook updates...")
    app.run(host="0.0.0.0", port=8080)
