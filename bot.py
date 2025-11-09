from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio

# === Настройки ===
TOKEN = "8256079955:AAGrghwannJh_tub3Av460PRKLV0nGR_cc8"
WEBAPP_URL = "https://projectguard-mini.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚪 Войти в систему",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )

    await message.answer(
        "Привет 👋\n\nЭто Aquafloor ProjectGuard — система защиты проектов.\n"
        "Нажми кнопку ниже, чтобы войти в систему:",
        reply_markup=keyboard
    )

async def main():
    print("✅ Bot запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


