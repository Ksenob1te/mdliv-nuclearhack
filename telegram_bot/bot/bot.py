import json
import logging
from telebot.async_telebot import AsyncTeleBot
from telegram_bot.database import crud
from telegram_bot.database.db import get_async_session, async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from telegram_bot import text
from telebot.types import Message
import requests
from app.params import BOT_TOKEN, PUBLIC_BOT_URL, PUBLIC_SERVER_URL


logger = logging.getLogger("TelegramBot")
bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
async def handler_start(message: Message) -> None:
    await bot.send_message(message.chat.id, text.start_message)


@bot.message_handler(content_types=['text'])
async def handler_main(message: Message) -> None:
    json_data = {"text": message.text, "webhook_url": f"http://{PUBLIC_BOT_URL}/bot/hook"}
    await bot.send_message(message.chat.id, text.request_committed)

    result = requests.post(url=f"http://{PUBLIC_SERVER_URL}/api/send", headers={'Content-Type': 'application/json'},
                           data=json.dumps(json_data))
    json_result = json.loads(result.text)
    if "ray_id" in json_result:
        async with async_session_maker() as session:
            await crud.create_ray_tracker(session, message.chat.id, json_result["ray_id"])
            await session.commit()


if BOT_TOKEN is None:
    logger.error("Bot token is not provided, bot not initialized")

