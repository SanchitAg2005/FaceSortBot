from utils.db import users

async def start(update, context):
    chat_id = update.effective_chat.id
    first = update.effective_user.first_name
    username = update.effective_user.username

    users.update_one(
        {"chat_id": chat_id},
        {
            "$setOnInsert": {
                "chat_id": chat_id,
                "first_name": first,
                "username": username,
                "activated": True
            }
        },
        upsert=True
    )

    await update.message.reply_text(
    f"👋 Hey {first}!\n"
    f"Your Telegram ID is: `{chat_id}`\n\n"
    f"Keep this ID safe — it will be needed inside FaceSort."
)
