import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .config import settings
from .views import setup_views
from .service.utils import check_bot_access, startup_redis, shutdown_redis, \
    make_db_account_redis


def setup_tortoise(api: FastAPI):
    register_tortoise(
        api,
        config=settings.DATABASE,
        modules={'models': ['app.models']},
        generate_schemas=False
    )


def register_events(api):
    api.on_event('startup')(check_bot_access)
    api.on_event('startup')(startup_redis)
    api.on_event('startup')(make_db_account_redis)
    api.on_event('shutdown')(shutdown_redis)


def setup_app() -> FastAPI:
    api = FastAPI(title="Telegram ticket bot",
                  docs_url="/ticket-bot/docs",
                  openapi_url="/ticket-bot/openapi.json",
                  version="1.0.0")
    setup_tortoise(api)
    setup_views(api)
    register_events(api)
    return api


def main():
    uvicorn.run(
        setup_app(),
        host=settings.HOST,
        port=settings.PORT,
    )
