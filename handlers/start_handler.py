from utils.db import users
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    first = update.effective_user.first_name
    username = update.effective_user.username

    users.update_one(
        {"chat_id": chat_id},
        {"$set": {"first_name": first, "username": username, "activated": True}},
        upsert=True
    )

    await update.message.reply_text(
        f"👋 Hey {first or 'there'}!\n\n"
        f"Your Telegram ID:\n`{chat_id}`\n\n"
        f"You are now registered!",
        parse_mode="Markdown"
    )
