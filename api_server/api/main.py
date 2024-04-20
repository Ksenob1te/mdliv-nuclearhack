from fastapi import APIRouter
import uuid
from pydantic import BaseModel
from api_server.database.db import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
import api_server.database.crud as crud
import api_server.endpoints as endpoints

from app.params import API_IP, API_PORT

router = APIRouter()


class SendRequest(BaseModel):
    text: str
    webhook_url: str


class SendResponse(BaseModel):
    ray_id: str


class NeuroMessage(BaseModel):
    role: str
    content: str


class NeuroChoice(BaseModel):
    index: int
    message: NeuroMessage
    finish_reason: str


class NeuroAnswer(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[NeuroChoice]
    usage: Any


@router.post("/send")
def send(req: SendRequest, session: AsyncSession = Depends(get_async_session)) -> SendResponse:
    user_ray_id = uuid.uuid4().hex
    neuro_ray_id = uuid.uuid4().hex

    log_inst = crud.make_log(session, req.text, user_ray_id, neuro_ray_id)

    return SendResponse(ray_id=user_ray_id)


@router.post("/neuro/hook/preprocess")
def neuro_hook_preprocess(req: NeuroAnswer):
    pass


@router.post("/neuro/hook/process")
def neuro_hook_process(req: NeuroAnswer):
    pass
