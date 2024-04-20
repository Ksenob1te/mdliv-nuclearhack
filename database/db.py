from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.schema import Base
from app.params import (DB_HOST, DB_NAME, DB_PORT, DB_TYPE, DB_USER_LOGIN,
                        DB_USER_PASSWORD)

from typing import Annotated
from fastapi import Depends

connect_string = ""

if DB_TYPE == "mysql":
    connect_string = f"mysql+pymysql://{DB_USER_LOGIN}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    connect_string = f"sqlite+aiosqlite:///./{DB_NAME}2.db"


engine = create_async_engine(connect_string, echo=True, connect_args={
                             "check_same_thread": False})
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
        
AsyncSession = Annotated[async_session_maker, Depends(get_async_session)]