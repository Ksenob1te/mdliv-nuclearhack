from api_server.database.crud import *
from api_server.database.db import async_session_maker
# from api_server.database.schema import *
import asyncio


async def main():
    # print("[", end="")
    # async with async_session_maker() as session:
    #     stmt = select(MetroStation, MetroLine.line_number, MetroLine.name).join(MetroLine, MetroLine.id == MetroStation.line_id)
    #     res = await session.execute(stmt)
    #     for x in res:
    #         print(
    #             f"{'('}{x[0].name}, {x[2]}, {x[1]}{')'},",
    #             end=" ")
    # print("]", end="")
    station_list = set()
    line_list = set()
    async with async_session_maker() as session:
        stmt = select(MetroStation)
        res = await session.execute(stmt)
        for x in res:
            station_list.add(x[0].name)

        stmt = select(MetroLine)
        res = await session.execute(stmt)
        for x in res:
            line_list.add((x[0].name, x[0].line_number))
    print(station_list)
    print(line_list)

        # x = next(res)
        # while x:
        #     x = next(res)

asyncio.run(main())