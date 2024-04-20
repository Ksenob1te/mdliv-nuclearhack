from dotenv import load_dotenv
import os
import logging

load_dotenv()

DB_HOST = os.environ.get("DATABASE_HOST", "localhost")
DB_NAME = os.environ.get("DATABASE_TABLE", "flow")
DB_PORT = int(os.environ.get("DATABASE_PORT", "3306"))
DB_TYPE = os.environ.get("DATABASE_TYPE", "sqlite")
DB_USER_LOGIN = os.environ.get("DATABASE_USERNAME", "root")
DB_USER_PASSWORD = os.environ.get("DATABASE_PASSWORD", "root")

API_IP = os.environ.get("MAIN_API_IP", "localhost")
API_PORT = int(os.environ.get("MAIN_API_PORT", "8080"))

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

logging.basicConfig(
    filename="log.txt",
    filemode='a',
    format='%(asctime)s,%(msecs)d - %(name)s - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

DEBUG = bool(os.environ.get("DEBUG", "False"))