from utils.db import users

async def start(update, context):
    print("⚡ /start handler triggered")

    user = update.effective_user

    # Insert only if new user
    users.update_one(
        {"_id": user.id},
        {"$set": {"name": user.first_name}},
        upsert=True
    )

    print(f"🟢 User saved: {user.id} - {user.first_name}")

    await update.message.reply_text(
        f"🎉 Welcome {user.first_name}!\n"
        f"🆔 Your Telegram ID is: `{user.id}`",
        parse_mode="Markdown"
    )
