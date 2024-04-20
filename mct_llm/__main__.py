import uvicorn

from app.params import DEBUG, NEURO_PORT

if __name__ == "__main__":
    uvicorn.run("mct_llm.app:app", host="0.0.0.0", port=NEURO_PORT, reload=DEBUG)