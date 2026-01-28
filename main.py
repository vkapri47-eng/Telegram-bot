import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Router

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = "https://api.b77bf911.workers.dev"

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN not set!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


def format_json(data, level=0):
    indent = "  " * level
    formatted = ""
    if isinstance(data, dict):
        for k, v in data.items():
            formatted += f"{indent}• {k}: "
            if isinstance(v, (dict, list)):
                formatted += "\n" + format_json(v, level + 1)
            else:
                formatted += f"{v}\n"
    elif isinstance(data, list):
        for i, item in enumerate(data):
            formatted += f"{indent}[{i}]\n"
            formatted += format_json(item, level + 1)
    else:
        formatted += f"{indent}{data}\n"
    return formatted


def pretty(data):
    try:
        return f"```\n{format_json(data)}\n```"
    except:
        return str(data)


async def fetch(endpoint, key, value):
    try:
        url = f"{BASE_URL}/{endpoint}?{key}={value}"
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer(
        "**Welcome to Data Lookup Bot!**\n"
        "Commands:\n"
        "📱 /mobile\n🆔 /aadhaar\n🧾 /gst\n🪪 /pan\n🚘 /vehicle\n🏦 /ifsc\n💬 /telegram\n💳 /upi\n💳 /upi2\n🍚 /rashan\n🔍 /v2\n\n"
        "Example: `/mobile 9876543210`",
        parse_mode=ParseMode.MARKDOWN
    )


commands_map = {
    "mobile": ("mobile", "number"),
    "aadhaar": ("aadhaar", "id"),
    "gst": ("gst", "number"),
    "pan": ("pan", "pan"),
    "vehicle": ("vehicle", "registration"),
    "ifsc": ("ifsc", "code"),
    "telegram": ("telegram", "user"),
    "upi": ("upi", "id"),
    "upi2": ("upi2", "id"),
    "rashan": ("rashan", "aadhaar"),
    "v2": ("v2", "query"),
}


@router.message()
async def commands_handler(msg: types.Message):
    text = msg.text.split(maxsplit=1)
    if not text[0].startswith("/"):
        return

    cmd = text[0][1:]
    if cmd not in commands_map:
        return

    if len(text) < 2:
        return await msg.answer(f"Usage: `/{cmd} <value>`", parse_mode=ParseMode.MARKDOWN)

    endpoint, param = commands_map[cmd]
    data = await fetch(endpoint, param, text[1])
    await msg.answer(pretty(data), parse_mode=ParseMode.MARKDOWN)


async def main():
    print("🚀 BOT STARTED & POLLING...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
