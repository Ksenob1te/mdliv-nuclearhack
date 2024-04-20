from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from telegram_bot.database.schema import Base
from app.params import (BOT_DB_HOST, BOT_DB_USER_LOGIN, BOT_DB_USER_PASSWORD,
                        BOT_DB_PORT, BOT_DB_NAME, BOT_DB_TYPE)

from typing import Annotated
from fastapi import Depends

connect_string = ""

if BOT_DB_TYPE == "mysql":
    connect_string = f"mysql+pymysql://{BOT_DB_USER_LOGIN}:{BOT_DB_USER_PASSWORD}@{BOT_DB_HOST}:{BOT_DB_PORT}/{BOT_DB_NAME}"
else:
    connect_string = f"sqlite+aiosqlite:///./{BOT_DB_NAME}.db"

engine = create_async_engine(connect_string, echo=True, connect_args={
    "check_same_thread": False})
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
