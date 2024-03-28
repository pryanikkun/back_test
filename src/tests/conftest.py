import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise


# from app.config import DATABASE
# from app.main import setup_views
#
# def setup_tortoise(api: FastAPI):
#     register_tortoise(
#         api,
#         config=DATABASE,
#         modules={'models': ['app.models']},
#         generate_schemas=False
#     )
#
#
# def setup_app():
#     app = FastAPI(title="Telegram ticket bot",
#                   docs_url="/ticket-bot/docs",
#                   openapi_url="/ticket-bot/openapi.json",
#                   version="1.0.0")
#     setup_tortoise(app)
#     setup_views(app)
#     return app


try:
    from app.main import setup_app
    app = setup_app()
except ImportError as ie:
    msg = 'Функция `setup_app` не обнаружена.'
    raise AssertionError(msg) from ie


@pytest.fixture(scope="session")
def client_app():
    """Возвращает клиента для тестирования."""
    with TestClient(app) as client:
        return client