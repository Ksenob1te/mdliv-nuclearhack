from telegram_bot.database.schema import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_chat_id_by_ray_id(session: AsyncSession, ray_id: str) -> int | None:
    stmt = select(RayTracker).where(RayTracker.ray_id == ray_id).order_by(RayTracker.id.desc()).limit(1)
    res = await session.scalar(stmt)
    return res.chat_id


async def create_ray_tracker(session: AsyncSession, chat_id: int, ray_id: str) -> None:
    new_instance = RayTracker()
    new_instance.ray_id = ray_id
    new_instance.chat_id = chat_id
    session.add(new_instance)
