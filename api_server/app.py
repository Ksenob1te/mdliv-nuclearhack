from fastapi import FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager
from api_server.api.main import router as api_router
from api_server.database.db import engine, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await engine.connect()
    await create_db_and_tables()
    yield
    # Clean up the ML models and release the resources
    await engine.dispose()


app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})

    