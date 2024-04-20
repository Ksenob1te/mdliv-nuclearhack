from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from telegram_bot.database import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from telegram_bot.database.db import get_async_session
from telegram_bot.bot.bot import bot

from contextlib import asynccontextmanager
from telegram_bot.database.db import engine, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.connect()
    await create_db_and_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


class GetRequest(BaseModel):
    text: str
    ray_id: str


@app.post("/bot/hook")
async def send(req: GetRequest, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    chat_id = await crud.get_chat_id_by_ray_id(session, req.ray_id)
    await bot.send_message(chat_id, f"NEW RESPONSE JUST DROPPED: {req.text}")
    return JSONResponse(content={"result": 1})


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
