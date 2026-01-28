import os
import requests
from aiogram import Bot, Dispatcher, executor, types

# ====== ENVIRONMENT VARIABLES ======
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway se aayega
BASE_URL = "https://api.b77bf911.workers.dev"

# ====== INIT BOT ======
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# ---------- FORMATTER FUNCTIONS ----------
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


# ---------- API WRAPPER ----------
async def fetch(endpoint, key, value):
    try:
        url = f"{BASE_URL}/{endpoint}?{key}={value}"
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ---------- COMMANDS ----------
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply(
        "**Welcome to Data Lookup Bot!**\n"
        "Available Commands:\n\n"
        "📱 `/mobile <number>`\n"
        "🆔 `/aadhaar <id>`\n"
        "🧾 `/gst <number>`\n"
        "🪪 `/pan <pan>`\n"
        "🚘 `/vehicle <reg>`\n"
        "🏦 `/ifsc <code>`\n"
        "💬 `/telegram <user>`\n"
        "💳 `/upi <id>`\n"
        "💳 `/upi2 <id>`\n"
        "🍚 `/rashan <aadhaar>`\n"
        "🔍 `/v2 <query>`\n\n"
        "Example: `/mobile 9876543210`",
        parse_mode="Markdown"
    )


@dp.message_handler(commands=['mobile'])
async def mobile_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/mobile <number>`", parse_mode="Markdown")
    data = await fetch("mobile", "number", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['aadhaar'])
async def aadhaar_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/aadhaar <id>`", parse_mode="Markdown")
    data = await fetch("aadhaar", "id", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['gst'])
async def gst_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/gst <number>`", parse_mode="Markdown")
    data = await fetch("gst", "number", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['pan'])
async def pan_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/pan <pan>`", parse_mode="Markdown")
    data = await fetch("pan", "pan", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['vehicle'])
async def vehicle_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/vehicle <reg>`", parse_mode="Markdown")
    data = await fetch("vehicle", "registration", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['ifsc'])
async def ifsc_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/ifsc <code>`", parse_mode="Markdown")
    data = await fetch("ifsc", "code", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['telegram'])
async def telegram_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/telegram <user>`", parse_mode="Markdown")
    data = await fetch("telegram", "user", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['upi'])
async def upi_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/upi <id>`", parse_mode="Markdown")
    data = await fetch("upi", "id", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['upi2'])
async def upi2_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/upi2 <id>`", parse_mode="Markdown")
    data = await fetch("upi2", "id", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['rashan'])
async def rashan_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Usage: `/rashan <aadhaar>`", parse_mode="Markdown")
    data = await fetch("rashan", "aadhaar", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


@dp.message_handler(commands=['v2'])
async def v2_cmd(msg: types.Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.reply("Usage: `/v2 <query>`", parse_mode="Markdown")
    data = await fetch("v2", "query", args[1])
    await msg.reply(pretty(data), parse_mode="Markdown")


# ---------- RUN BOT ----------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
