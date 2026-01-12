import os
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler

from handlers.start_handler import start

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

async def handle(request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
    except Exception as e:
        print("⚠️ Error handling update:", e)
    return web.Response(text="ok")

async def on_startup(app):
    print("🚀 FaceSort Bot initialized")
    await bot_app.initialize()
    await bot_app.start()
    print("🌍 Setting webhook at:", WEBHOOK_URL)
    await bot_app.bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot_app.stop()
    await bot_app.shutdown()

# Telegram Bot Application
bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# aiohttp Web Server
app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    print("🔥 Running FaceSort Bot HTTP Server...")
    web.run_app(app, host="0.0.0.0", port=8080)
