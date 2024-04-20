from api_server.database.schema import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def make_log(session: AsyncSession, text: str, user_ray_id: str, neuro_ray_id: str, webhook: str) -> History:
    log = History(request=text, user_ray_id=user_ray_id,
                  neuro_ray_id=neuro_ray_id, webhook=webhook)
    session.add_all([log])
    return log


async def get_log_by_neuro_ray_id(session: AsyncSession, neuro_ray_id: str) -> History | None:
    stmt = select(History).where(History.neuro_ray_id == neuro_ray_id)
    res = await session.scalar(stmt)
    return res


async def create_metro_station(session: AsyncSession, name: str, line_id: str):
    station = MetroStation(name=name, line_id=line_id)
    session.add_all([station])
    return station


async def create_metro_line(session: AsyncSession, name: str, line_number: int):
    station = MetroLine(name=name, line_number=line_number)
    session.add_all([station])
    return station


async def get_metro_line_by_number(session: AsyncSession, line_number: int) -> MetroLine | None:
    stmt = select(MetroLine).where(MetroLine.line_number == line_number)
    res = await session.scalar(stmt)
    return res


async def get_metro_line_by_id(session: AsyncSession, id: int) -> MetroLine | None:
    stmt = select(MetroLine).where(MetroLine.id == id)
    res = await session.scalar(stmt)
    return res


async def get_metro_station_by_id(session: AsyncSession, id: int) -> MetroStation | None:
    stmt = select(MetroStation).where(MetroStation.id == id)
    res = await session.scalar(stmt)
    return res


async def create_flow_record(session: AsyncSession, station_id: int, timestamp: datetime, count: int) -> FlowData:
    station = FlowData(metro_station_id=station_id, timestamp=timestamp, count=count)
    session.add_all([station])
    return station


async def get_flow_record(session: AsyncSession, station_id: int, timestamp: datetime) -> FlowData:
    stmt = select(FlowData).where(FlowData.metro_station_id == station_id).where(FlowData.timestamp == timestamp)
    res = await session.scalar(stmt)
    return res


async def get_station_by_name(session: AsyncSession, name: str) -> MetroStation:
    stmt = select(MetroStation).where(MetroStation.name == name).limit(1)
    res = await session.scalar(stmt)
    return res
