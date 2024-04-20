import uvicorn

from app.params import API_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run("api_server.app:app", host="0.0.0.0", port=API_PORT, reload=DEBUG)