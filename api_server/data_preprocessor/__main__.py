from api_server.database.crud import *
from api_server.database.db import * 
from api_server.database.schema import *
from typing import List, Dict
import pandas as pd

import asyncio


async def main():
    await create_db_and_tables()
    async with async_session_maker() as session:
        unique_metro_station_id = {}

        df: pd.DataFrame = pd.read_csv('stations.csv', delimiter=';')
        df.rename(columns={'Станция': 'station_name', 'Номер линии': 'line_num', 'Дата': 'line_name'}, inplace=True)
        df = df.sort_values(by=['station_name', 'line_num', 'line_name'], ascending=False)
        df = df.groupby(['station_name', 'line_name'], as_index=False).first()
        station_list: List[List[str]] = zip(df['station_name'].values.tolist(),
                                            df['line_num'].values.tolist(),
                                            df['line_name'].values.tolist())

        station_dict: Dict[(str, int), int] = {}

        for station_name, line_num, line_name in station_list:
            if (line_name, line_num) not in station_dict:
                metro_line = await create_metro_line(session, line_name, line_num)
                await session.commit()
                await session.refresh(metro_line)
                line_id: int = metro_line.id
                station_dict[(line_name, line_num)] = line_id
            else:
                line_id: int = station_dict[(line_name, line_num)]
            metro_station = (await create_metro_station(session, station_name, str(line_id)))
            await session.commit()
            await session.refresh(metro_station)
            unique_metro_station_id[(station_name, line_name, line_num)] = metro_station.id

        header = df.columns.tolist()
        for index, row in df.iterrows():
            ok = row.tolist()
            cel = (ok[0], ok[1], ok[2])
            need_id = unique_metro_station_id[cel]
            for j in range(3, len(ok)):
                # timestamp = header[j]
                timestamp = datetime.strptime(header[j], "%d.%m.%Y")
                # print(timestamp)
                count = ok[j]
                await create_flow_record(session, need_id, timestamp, count)
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
