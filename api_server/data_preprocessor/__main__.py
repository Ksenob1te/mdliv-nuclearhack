from api_server.database.crud import *
from api_server.database.db import * 
from api_server.database.schema import *
import pandas as pd

import asyncio


async def main():
    await create_db_and_tables()
    async with async_session_maker() as session:

        unique_metro_station_id = {}

        df = pd.read_csv('stations.csv')
        df.rename(columns={'Станция': 'station_name', 'Номер линии': 'line_num', 'Дата': 'line_name'}, inplace=True)
        # сортируем по (станция, линия), чтобы убрать дубли
        df = df.sort_values(by=['station_name', 'line_num', '4/3/2024'], ascending=False)
        df = df.groupby(['station_name', 'line_name'], as_index=False).first()

        stationName_num_nameLine = zip(df['station_name'].values.tolist(), df['line_num'].values.tolist(), df['line_name'].values.tolist())

        for stationName, num, Linename in stationName_num_nameLine:
            metro_line = await create_metro_line(session, num, Linename)
            await session.commit()
            await session.refresh(metro_line)
            print(metro_line.id)
            metro_station = (await create_metro_station(session, stationName, metro_line.id))
            await session.commit()
            await session.refresh(metro_station)
            unique_metro_station_id[(stationName, Linename, num)] = metro_station.id

        header = df.columns.tolist()
        for index, row in df.iterrows():
            ok = row.tolist()
            cel = (ok[0], ok[1], ok[2])
            need_id = unique_metro_station_id[cel]
            for j in range(3, len(ok)):
                timestamp = header[j]
                count = ok[j]
                await create_flow_record(session, need_id, count, timestamp)
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
