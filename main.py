import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from aiogram.utils.formatting import as_markdown
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = "https://api.b77bf911.workers.dev"

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
        text = format_json(data)
        return f"```\n{text}\n```"
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
async def start(msg: types.Message):
    await msg.answer(
        "**Welcome to Data Lookup Bot!**\n"
        "Commands:\n"
        "📱 /mobile\n🆔 /aadhaar\n🧾 /gst\n🪪 /pan\n🚘 /vehicle\n🏦 /ifsc\n💬 /telegram\n💳 /upi\n💳 /upi2\n🍚 /rashan\n🔍 /v2",
        parse_mode=ParseMode.MARKDOWN
    )

CMD_LIST = {
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
    "v2": ("v2", "query")
}

@router.message()
async def all_commands(msg: types.Message):
    text = msg.text.split(maxsplit=1)
    cmd = text[0][1:] if text[0].startswith("/") else None
    
    if cmd in CMD_LIST:
        if len(text) < 2:
            return await msg.answer(f"Usage: `/{cmd} <value>`", parse_mode=ParseMode.MARKDOWN)
        
        endpoint, param = CMD_LIST[cmd]
        data = await fetch(endpoint, param, text[1])
        return await msg.answer(pretty(data), parse_mode=ParseMode.MARKDOWN)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
