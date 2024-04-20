import uvicorn

from app.params import BOT_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run("telegram_bot.server.app:app", port=BOT_PORT, reload=DEBUG)
