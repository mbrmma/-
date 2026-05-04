import asyncio
import json
import logging
import os
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "2107362512"))
WEB_APP_URL = os.getenv("WEB_APP_URL")

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "8080"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🍓 Открыть мини-апп", web_app=WebAppInfo(url=WEB_APP_URL))

    await message.answer(
        "Нажми кнопку ниже, чтобы открыть магазин 👇",
        reply_markup=kb.as_markup()
    )


@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except:
        await message.answer("Ошибка заказа")
        return

    text = (
        f"<b>Новый заказ</b>\n\n"
        f"Имя: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Комментарий: {data.get('comment')}\n\n"
        f"Итого: {data.get('total')} ₽"
    )

    await message.answer("Заказ отправлен ✅")
    await bot.send_message(ADMIN_ID, text)


# ---------- ВАЖНО: ВЕБ-СЕРВЕР ----------

async def index(request):
    return web.FileResponse(BASE_DIR / "index.html")

async def style(request):
    return web.FileResponse(BASE_DIR / "style.css")

async def start_web():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/index.html", index)
    app.router.add_get("/style.css", style)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()

    print(f"Сервер запущен на порту {PORT}")


async def main():
    await start_web()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())