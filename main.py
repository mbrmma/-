import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import os
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍓 Купить клубнику")],
        [KeyboardButton(text="📦 Мой заказ")]
    ],
    resize_keyboard=True
)

@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        await message.answer("Добро пожаловать 🍓\nВыберите действие:", reply_markup=kb)

    elif message.text == "🍓 Купить клубнику":
        await message.answer(
            "Выберите фасовку:\n\n"
            "0.5 кг — 500₽\n"
            "1 кг — 1000₽\n"
            "1.5 кг — 1500₽\n"
            "2 кг — 2000₽"
        )

    elif message.text == "📦 Мой заказ":
        await message.answer("У вас пока нет заказов 😔")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
