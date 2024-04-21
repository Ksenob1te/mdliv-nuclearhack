from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException
import uuid
from pydantic import BaseModel
from api_server.database.db import get_async_session
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
import api_server.database.crud as crud
import api_server.endpoints as endpoints
import json
from datetime import datetime
from app.params import PUBLIC_SERVER_URL, API_PORT, PUBLIC_NEURO_URL

router = APIRouter()


class SendRequest(BaseModel):
    text: str
    webhook_url: str


class SendResponse(BaseModel):
    ray_id: str


class NeuroRequest(BaseModel):
    webhook: str
    content: str
    base_prompt: str
    ray_id: str


class NeuroAnswer(BaseModel):
    ray_id: str
    result: str


BASE_PROMPT_PREPROCESSOR = "Answer the following question in json format by highlighting the station name in the station key, and the date specified in the message in the date key, converting the date to the time format like YYYY-MM-DD. Название станции в именительном падеже"
BASE_PROMPT_PROCESSOR = ""
SYSTEM_PREPROCESSOR = "Today is April 3, 2024. You print only json."
SYSTEM_PROCESSOR = "Today is April 3, 2024. В день {}, было {} людей на станции {} station. Answer only in Russian. Отвечай на русском."

@router.post("/send")
async def send(req: SendRequest, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)) -> SendResponse:
    user_ray_id = uuid.uuid4().hex
    neuro_ray_id = uuid.uuid4().hex

    log_inst = await crud.make_log(session, req.text, user_ray_id, neuro_ray_id, req.webhook_url)

    await session.commit()
    background_tasks.add_task(
        endpoints.send_to_neuro, f"http://{PUBLIC_NEURO_URL}/process", f"http://{PUBLIC_SERVER_URL}/api/neuro/hook/preprocess",
        BASE_PROMPT_PREPROCESSOR + "\n" + req.text, neuro_ray_id, SYSTEM_PREPROCESSOR
    )
    return SendResponse(ray_id=user_ray_id)


@router.post("/neuro/hook/preprocess")
async def neuro_hook_preprocess(req: NeuroAnswer, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    log_inst = await crud.get_log_by_neuro_ray_id(session, req.ray_id)
    if log_inst is None:
        raise HTTPException(400)
    if log_inst.response is not None:
        raise HTTPException(400)
    
    try:
        data = json.loads(req.result.strip())
        date = datetime.fromisoformat(data["date"])
        station = data["station"].strip().replace(" ", "-")
    except Exception as e:
        print(e)
        data = None
    
    if data is None:
        background_tasks.add_task(
            endpoints.send_to_telegram, log_inst.webhook, "Внутреняя ошибка сервера. Попробуйте еще раз", log_inst.user_ray_id
        )
        return JSONResponse({"msg": "ok"})
    
    st = await crud.get_station_by_name(session, station)
    
    if st is None:
        print("Dont have station data")
        background_tasks.add_task(
            endpoints.send_to_telegram, log_inst.webhook, "Внутреняя ошибка сервера. Попробуйте еще раз", log_inst.user_ray_id
        )
        return JSONResponse({"msg": "ok"})
    
    fr = await crud.get_flow_record(session, st.id, datetime.fromisoformat(data["date"]))
    if fr is None:
        print("Dont have time data")
        background_tasks.add_task(
            endpoints.send_to_telegram, log_inst.webhook, "Внутреняя ошибка сервера. Попробуйте еще раз", log_inst.user_ray_id
        )
        return JSONResponse({"msg": "ok"})
    prompt = BASE_PROMPT_PROCESSOR
    
    date = "{} days {} months {}".format(date.day, date.month, date.year)
    system_prompt = SYSTEM_PROCESSOR.format(date, 1231, station)
    prompt = prompt + "\n" + req.result
    
    background_tasks.add_task(
        endpoints.send_to_neuro, f"http://{PUBLIC_NEURO_URL}/process", f"http://{PUBLIC_SERVER_URL}/api/neuro/hook/process",
        prompt, log_inst.neuro_ray_id, system_prompt
    )
    return JSONResponse({"msg": "ok"})


@router.post("/neuro/hook/process")
async def neuro_hook_process(req: NeuroAnswer, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    log_inst = await crud.get_log_by_neuro_ray_id(session, req.ray_id)
    if log_inst is None:
        raise HTTPException(400)
    if log_inst.response is not None:
        raise HTTPException(400)

    log_inst.response = req.result
    background_tasks.add_task(
        endpoints.send_to_telegram, log_inst.webhook, req.result, log_inst.user_ray_id
    )
    await session.commit()
    return JSONResponse({"msg": "ok"})
