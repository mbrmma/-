import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"
WEB_APP_URL = "https://ТВОЙ_АДРЕС/index.html"
ADMIN_ID = 2107362512

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🍓 Открыть мини-апп", web_app=WebAppInfo(url=WEB_APP_URL))

    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы оформить заказ клубники.",
        reply_markup=kb.as_markup()
    )


@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        await message.answer("Не удалось прочитать данные заказа.")
        return

    name = data.get("name", "")
    phone = data.get("phone", "")
    comment = data.get("comment", "")
    items = data.get("items", {})
    total = data.get("total", 0)

    order_text = (
        "<b>Новый заказ</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>Комментарий:</b> {comment or '-'}\n\n"
        "<b>Состав заказа:</b>\n"
        f"0.5 кг: {items.get('0.5 кг', 0)}\n"
        f"1 кг: {items.get('1 кг', 0)}\n"
        f"1.5 кг: {items.get('1.5 кг', 0)}\n"
        f"2 кг: {items.get('2 кг', 0)}\n\n"
        f"<b>Итого:</b> {total} ₽"
    )

    await message.answer("Заказ отправлен ✅")
    await bot.send_message(ADMIN_ID, order_text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())