from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from llama_cpp import Llama
import asyncio
import json
from app.params import PUBLIC_SERVER_URL


loop = asyncio.get_event_loop()
app = FastAPI()

llm = Llama(
    model_path="codellama-7b-instruct.Q4_K_S.gguf",
    use_mlock=True
)


class NeuroRequest(BaseModel):
    webhook: str
    content: str
    ray_id: str


class NeuroAnswer(BaseModel):
    ray_id: str
    result: str


async def process_prompt(req: NeuroRequest):
    print("Starting processing")
    llm_response = llm.create_chat_completion(
        messages=[
            {"role": "system",
                "content": "Ты отлично классифицируешь сообщения по категориям."},
            {
                "role": "user",
                "content": req.content
            }
        ],
    )
    response = llm_response['choices'][0]['message']['content']
    print(response)
    requests.post(url=req.webhook, headers={'Content-Type': 'application/json'},
                  data=json.dumps({"result": response, "ray_id": req.ray_id}))


@app.post("/process")
async def process(req: NeuroRequest, background_tasks: BackgroundTasks) -> JSONResponse:
    background_tasks.add_task(process_prompt, req)
    return JSONResponse({"msg": "ok"})


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
