import logging
from telebot.async_telebot import AsyncTeleBot
from telegram_bot import text
from telebot.types import Message
from app.params import BOT_TOKEN


logger = logging.getLogger("TelegramBot")
bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
async def handler_start(message: Message) -> None:
    await bot.send_message(message.chat.id, text.start_message)


@bot.message_handler(content_types=['text'])
async def handler_main(message: Message) -> None:
    await bot.send_message(message.chat.id, f"IVE GOT IT: {message.text}")


if BOT_TOKEN is None:
    logger.error("Bot token is not provided, bot not initialized")
else:
    import asyncio
    asyncio.run(bot.polling(non_stop=True))
