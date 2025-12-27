import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start_handler import start

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)

# Build bot app
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

@app.post("/")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put_nowait(update)
    return "ok", 200

if __name__ == "__main__":
    # 🚀 start webhook + start dispatcher worker
    import asyncio
    async def run():
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.bot.set_webhook(WEBHOOK_URL)
        await asyncio.Event().wait()

    asyncio.run(run())
