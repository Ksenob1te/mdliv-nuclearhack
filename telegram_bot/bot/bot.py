import json
import logging
from telebot.async_telebot import AsyncTeleBot
from telegram_bot.database import crud
from telegram_bot.database.db import get_async_session
from telegram_bot import text
from telebot.types import Message
import requests
from app.params import BOT_TOKEN


logger = logging.getLogger("TelegramBot")
bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
async def handler_start(message: Message) -> None:
    await bot.send_message(message.chat.id, text.start_message)


@bot.message_handler(content_types=['text'])
async def handler_main(message: Message) -> None:
    async_session = get_async_session()
    json_data = {"text": message.text, "webhook_url": ""}
    result = requests.post(url="http://192.168.238.10:8080/api/send", headers={'Content-Type': 'application/json'},
                           data='{"text": "string", "webhook_url": "string"}')
    print(json.loads(result.text)["ray_id"])
    await bot.send_message(message.chat.id, f"IVE GOT IT: {message.text}")


if BOT_TOKEN is None:
    logger.error("Bot token is not provided, bot not initialized")
else:
    import asyncio
    asyncio.run(bot.polling(non_stop=True))
