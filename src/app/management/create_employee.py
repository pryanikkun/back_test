import os
import hashlib
import asyncio
import time

from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from src.app.models import Employee
from src.app import redis

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
                'models': ['src.app.models', 'aerich.models'],
                'default_connection': 'default',
            }
        }
    }


async def setup_db():
    """ Подключение к Tortoise-ORM и redis """
    await Tortoise.init(
        config=DATABASE
    )
    redis_conn = await redis.init_pool_account_redis()
    redis.redis = redis.RedisStorage(redis_conn)


async def create_account(username: str, password: str):
    """ Создание сотрудника """
    hashed_password = hashlib.sha1(password.encode()).hexdigest()
    await setup_db()
    try:
        if username and password:
            await Employee.create(
                username=username,
                password=hashed_password
            )
            await redis.redis.set_account(username, hashed_password)
        else:
            print("Логин и/или пароль не могут быть пустыми")
    except IntegrityError:
        print(f"Пользователь с логином {username} существует")
    redis.redis.close()


async def main():
    time.sleep(1)
    username = input('Username: ')
    user_password = input('Password: ')
    await create_account(username, user_password)

asyncio.run(main())
