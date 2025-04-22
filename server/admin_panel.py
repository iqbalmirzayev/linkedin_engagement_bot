from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db_maker_account import add_account, get_all_accounts, remove_account_by_telegram_id

admin_router = Router()

ALLOWED_ADMINS = []  # Öz ID-n burada saxlanır

def is_admin(message: Message) -> bool:
    return message.from_user.id in ALLOWED_ADMINS

class AddAccountState(StatesGroup):
    waiting_for_telegram_id = State()
    waiting_for_telegram_id_like_comment = State()
    waiting_for_telegram_id_remove = State()

@admin_router.message(CommandStart())
async def start_handler(message: Message):
    if not is_admin(message): return
    await message.answer("👋 Salam admin!")

@admin_router.message(Command("help"))
async def help_handler(message: Message):
    if not is_admin(message): return
    await message.answer("🆘 Komandalar:\n/add_like_account\n/add_like_comment_account\n/remove_account\n/list_accounts")

@admin_router.message(Command("add_like_account"))
async def add_like_handler(message: Message, state: FSMContext):
    if not is_admin(message): return
    await message.answer("🧾 Like edəcək account-un Telegram ID-sini daxil et:")
    await state.set_state(AddAccountState.waiting_for_telegram_id)

@admin_router.message(AddAccountState.waiting_for_telegram_id)
async def save_like_id(message: Message, state: FSMContext):
    if not is_admin(message):
        await state.clear()
        return
    try:
        telegram_id = int(message.text.strip())
        add_account(telegram_id, "like")
        await message.answer(f"✅ {telegram_id} əlavə olundu (like).")
    except Exception:
        await message.answer("❌ Format yanlış.")
    finally:
        await state.clear()

@admin_router.message(Command("add_like_comment_account"))
async def add_like_comment_handler(message: Message, state: FSMContext):
    if not is_admin(message): return
    await message.answer("💬 Like + Comment edəcək account-un ID-sini daxil et:")
    await state.set_state(AddAccountState.waiting_for_telegram_id_like_comment)

@admin_router.message(AddAccountState.waiting_for_telegram_id_like_comment)
async def save_like_comment_id(message: Message, state: FSMContext):
    if not is_admin(message):
        await state.clear()
        return
    try:
        telegram_id = int(message.text.strip())
        add_account(telegram_id, "like_comment")
        await message.answer(f"✅ {telegram_id} əlavə olundu (like+comment).")
    except Exception:
        await message.answer("❌ Format yanlış.")
    finally:
        await state.clear()

@admin_router.message(Command("remove_account"))
async def remove_account(message: Message, state: FSMContext):
    if not is_admin(message): return
    await message.answer("❌ Silmək istədiyin Telegram ID-ni daxil et:")
    await state.set_state(AddAccountState.waiting_for_telegram_id_remove)

@admin_router.message(AddAccountState.waiting_for_telegram_id_remove)
async def process_remove(message: Message, state: FSMContext):
    if not is_admin(message):
        await state.clear()
        return
    try:
        telegram_id = int(message.text.strip())
        remove_account_by_telegram_id(telegram_id)
        await message.answer(f"🗑 {telegram_id} silindi.")
    except Exception:
        await message.answer("⚠️ Xəta baş verdi.")
    finally:
        await state.clear()

@admin_router.message(Command("list_accounts"))
async def list_accounts(message: Message):
    if not is_admin(message): return
    accounts = get_all_accounts()
    if not accounts:
        await message.answer("⚠️ Heç bir hesab tapılmadı.")
        return
    msg = "\n".join([f"🆔 {row[0]} | {row[1].upper()}" for row in accounts])
    await message.answer(f"📋 Əlavə olunmuş hesablar:\n{msg}")
