from telegram_bot.server.__main__ import run as server_run
from telegram_bot.bot.__main__ import run as bot_run
from multiprocessing import Process
import logging

if __name__ == "__main__":
    logger = logging.getLogger("globalBot")
    server_process = Process(target=server_run)
    bot_process = Process(target=bot_run)

    server_process.start()
    bot_process.start()
    server_process.join()
    bot_process.join()




