from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api_server.api.main import router as api_router



app =  FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"}) 