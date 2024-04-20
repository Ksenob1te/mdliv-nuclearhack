import logging

import telebot
from app.params import BOT_TOKEN


if BOT_TOKEN is None:
    logging.error()
bot = telebot.TeleBot()