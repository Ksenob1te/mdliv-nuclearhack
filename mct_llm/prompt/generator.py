from api_server.database.crud import *
from api_server.database.db import async_session_maker
# from api_server.database.schema import *
import asyncio


async def main():
    print("{", end="")
    async with async_session_maker() as session:
        stmt = select(MetroStation, MetroLine.line_number, MetroLine.name).join(MetroLine, MetroLine.id == MetroStation.line_id)
        res = await session.execute(stmt)
        for x in res:
            print(
                f"{'{'}station_name: {x[0].name}, line_name: {x[2]}, line_number:{x[1]}{'}'},",
                end=" ")
    print("}", end="")

        # x = next(res)
        # while x:
        #     x = next(res)

asyncio.run(main())