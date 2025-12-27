import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start_handler import start

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)
bot_app = None  # <-- create lazy global


def get_bot():
    global bot_app
    if bot_app is None:
        bot_app = ApplicationBuilder().token(TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.bot.set_webhook(url=WEBHOOK_URL)
    return bot_app


@app.post("/")
def webhook():
    application = get_bot()
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return "ok", 200


if __name__ == "__main__":
    get_bot()
    app.run(host="0.0.0.0", port=8080)
