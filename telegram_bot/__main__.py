from telegram_bot.server.__main__ import run as server_run
from telegram_bot.bot.__main__ import run as bot_run
from threading import Thread
import logging

if __name__ == "__main__":
    logger = logging.getLogger("globalBot")

    class BotServerThread(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self) -> None:
            logger.info("bot server started")
            server_run()


    class BotThread(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            logger.info("bot started")
            bot_run()

    server_thr = BotServerThread()
    bot_thr = BotThread()
    server_thr.run()
    bot_thr.run()


