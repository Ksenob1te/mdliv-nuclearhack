from fastapi import APIRouter
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


BASE_PROMPT_PREPROCESSOR = "Ответь на следующий вопрос в формате json выделив название станции в ключ station, а дату, указанную в сообщение в ключ date, преобразуя дату в европейский формат времени"
BASE_PROMPT_PROCESSOR = "Зная, что в дату {} на станции {} пассажиропоток был {} ответь на вопрос:"


@router.post("/send")
async def send(req: SendRequest, session: AsyncSession = Depends(get_async_session)) -> SendResponse:
    user_ray_id = uuid.uuid4().hex
    neuro_ray_id = uuid.uuid4().hex

    log_inst = await crud.make_log(session, req.text, user_ray_id, neuro_ray_id, req.webhook_url)

    await session.commit()
    
    endpoints.send_to_neuro(f"http://{PUBLIC_NEURO_URL}/process", f"http://{PUBLIC_SERVER_URL}/neuro/hook/preprocess", req.text, neuro_ray_id)

    return SendResponse(ray_id=user_ray_id)


@router.post("/neuro/hook/preprocess")
async def neuro_hook_preprocess(req: NeuroAnswer, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    log_inst = await crud.get_log_by_neuro_ray_id(session, req.ray_id)
    if log_inst is None:
        raise HTTPException(400)
    if log_inst.response is not None:
        raise HTTPException(400)
    
    
    
    endpoints.send_to_neuro(f"http://{PUBLIC_NEURO_URL}/process", f"http://{PUBLIC_SERVER_URL}/neuro/hook/process", req.text, log_inst.neuro_ray_id)
    
    return JSONResponse({"msg": "ok"})


@router.post("/neuro/hook/process")
async def neuro_hook_process(req: NeuroAnswer, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    log_inst = await crud.get_log_by_neuro_ray_id(session, req.ray_id)
    if log_inst is None:
        raise HTTPException(400)
    if log_inst.response is not None:
        raise HTTPException(400)
    
    log_inst.response = req.result
    
    endpoints.send_to_telegram(
        log_inst.webhook, req.result, log_inst.user_ray_id)
    
    await session.commit()
    return JSONResponse({"msg": "ok"})
