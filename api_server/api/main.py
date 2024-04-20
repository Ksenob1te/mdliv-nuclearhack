from fastapi import APIRouter
import uuid
from pydantic import BaseModel
from database.db import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
import database.crud as crud

router = APIRouter()


class SendRequest(BaseModel):
    text: str

class SendResponse(BaseModel):
    ray_id: str


class NeuroChoice(BaseModel):
    pass
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
def neuro_hook_preprocess():
    pass

@router.post("/neuro/hook/process")
def neuro_hook_process():
    pass