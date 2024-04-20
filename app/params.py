from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DATABASE_HOST", "localhost")
DB_NAME = os.environ.get("DATABASE_TABLE", "flow")
DB_PORT = os.environ.get("DATABASE_PORT", "3306")
DB_TYPE = os.environ.get("DATABASE_TYPE", "sqlite")
DB_USER_LOGIN, = os.environ.get("DATABASE_USERNAME", "root")
DB_USER_PASSWORD = os.environ.get("DATABASE_PASSWORD", "root")

API_IP = os.environ.get("MAIN_API_IP", "localhost")
API_PORT = os.environ.get("MAIN_API_PORT", "8080")