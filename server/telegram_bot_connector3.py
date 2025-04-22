import os
import re
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from storage import save_link  # LinkedIn linklərini DB-yə yazmaq üçün

collector_router = Router()

load_dotenv()
TARGET_THREAD_ID = 8132  # Botun cavab verəcəyi Telegram mövzu ID-si

@collector_router.message(CommandStart())
async def welcome_handler(message: Message):
    await message.answer("👋 Salam! Mən LinkedIn postlarını qeyd etmək üçün buradayam.")

@collector_router.message()
async def linkedin_link_handler(message: Message):
    # Yalnız spesifik mövzuya (thread) cavab verir
    if message.message_thread_id != TARGET_THREAD_ID:
        return

    telegram_id = message.from_user.id
    text = message.text

    linkedin_links = re.findall(r'https?://[^\s]*linkedin\.com[^\s]*', text)

    if linkedin_links:
        for link in linkedin_links:
            save_link(telegram_id, link)
            print(f"✅ [{telegram_id}] → Link saxlanıldı: {link}")
        #await message.answer("🔗 Link(ler) uğurla yadda saxlanıldı.")
    else:
        print(f"ℹ️ [{telegram_id}] mesaj yazdı, lakin link tapılmadı.")
