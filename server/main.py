import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from admin_panel import admin_router
from telegram_bot_connector3 import collector_router

# .env faylından tokeni yüklə
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API")

# Bot və Dispatcher obyektlərini yarat
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Router-ləri Dispatcher-ə əlavə et
dp.include_router(admin_router)
dp.include_router(collector_router)

# Botu işə sal
async def main():
    print("✅ Telegram bot başladı...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("⛔ Bot dayandırıldı.")
