import uvicorn

from app.params import BOT_SERVER_PORT, DEBUG


def run():
    uvicorn.run("telegram_bot.server.app:app", host="0.0.0.0", port=BOT_SERVER_PORT, reload=DEBUG)


if __name__ == "__main__":
    run()
