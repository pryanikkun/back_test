import os
import logging

from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE_DIR.parent) + '/.env')

DATABASE = {
        'connections': {
            # Dict format for connection
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': os.environ.get('POSTGRES_HOST', 'db'),
                    'port': os.environ.get('POSTGRES_PORT', '5432'),
                    'user': os.environ.get('POSTGRES_USER'),
                    'password': os.environ.get('POSTGRES_PASSWORD'),
                    'database': os.environ.get('POSTGRES_DB'),
                }
            },
            # Using a DB_URL string
            # 'default': 'postgres://postgres:qwerty123@localhost:5432/events'
        },
        'apps': {
            'models': {
                'models': ['app.models', 'aerich.models'],
                'default_connection': 'default',
            }
        }
    }


class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = int(os.environ.get('SERVICE_PORT', 80))

    DATABASE: dict = {}

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: str = '6379'

    TG_API: str = os.environ.get('TG_BOT_TOKEN')
    TG_ACCESS_URL: str = os.environ.get('TG_ACCESS_URL')


logging.basicConfig(level=logging.INFO)
logging.info('settings is called')

settings = Settings()


settings.DATABASE = DATABASE
