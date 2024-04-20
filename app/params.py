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

API_PORT = int(os.environ.get("MAIN_API_PORT", "8080"))
NEURO_PORT = int(os.environ.get("NEURO_API_PORT", "8082"))

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_SERVER_PORT = int(os.environ.get("BOT_SERVER_PORT", "8081"))

BOT_DB_HOST = os.environ.get("BOT_DB_HOST", "localhost")
BOT_DB_NAME = os.environ.get("BOT_DB_TABLE", "bot_base")
BOT_DB_PORT = int(os.environ.get("BOT_DB_PORT", "3306"))
BOT_DB_TYPE = os.environ.get("BOT_DB_TYPE", "sqlite")
BOT_DB_USER_LOGIN = os.environ.get("BOT_DB_USERNAME", "root")
BOT_DB_USER_PASSWORD = os.environ.get("BOT_DB_PASSWORD", "root")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(
    filename=os.path.join(ROOT_DIR, "log.txt"),
    filemode='a',
    format='%(asctime)s,%(msecs)d - %(name)s - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

DEBUG = os.environ.get("DEBUG", "False") == "TRUE"
PUBLIC_BOT_URL = os.environ.get("PUBLIC_BOT_URL", "localhost:8081")
PUBLIC_SERVER_URL = os.environ.get("PUBLIC_SERVER_URL", "localhost:8080")
PUBLIC_NEURO_URL = os.environ.get("PUBLIC_NEURO_URL", "localhost:8082")

