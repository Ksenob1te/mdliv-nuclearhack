from telegram_bot.bot.bot import bot


def run():
    import asyncio
    asyncio.run(bot.polling(non_stop=True))


if __name__ == "__main__":
    run()