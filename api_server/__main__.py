import uvicorn

from app.params import API_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run("api_server.app:app", port=API_PORT, reload=DEBUG)