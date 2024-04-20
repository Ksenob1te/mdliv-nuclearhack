from api_server.database.schema import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def make_log(session: AsyncSession, text: str, user_ray_id: str, neuro_ray_id: str) -> History:
    log = History(request=text, user_ray_id=user_ray_id,
                  neuro_ray_id=neuro_ray_id)
    session.add_all([log])

    await session.commit()

    return log


async def get_log_by_neuro_ray_id(session: AsyncSession, neuro_ray_id: str) -> History | None:
    stmt = select(History).where(History.neuro_ray_id == neuro_ray_id)
    res = await session.scalar(stmt)
    return res
