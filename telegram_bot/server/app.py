from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

# app.include_router(api_router, prefix="/bot")


class GetRequest(BaseModel):
    text: str
    ray_id: str


@app.post("/hook")
def send(req: GetRequest, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    log_inst = crud.make_log(session, req.text, user_ray_id, neuro_ray_id)

    return JSONResponse(content={"ABOBA": 1})


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
