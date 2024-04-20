from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# app.include_router(api_router, prefix="/bot")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
