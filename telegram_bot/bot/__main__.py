from telegram_bot.bot.bot import bot

if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.polling(non_stop=True))