from fastapi import HTTPException
import requests
import hashlib
from .. import redis
from ..models import Employee
from ..config import settings


def check_bot_access():
    r2 = requests.get(f'https://api.telegram.org/bot{settings.TG_API}/setWebhook?url={settings.TG_ACCESS_URL}/fox-ticket/')
    if r2.json()['ok']:
        pass
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Проблемы с подключением к боту (проверьте/обновите URL в .env)"
        )


async def startup_redis():
    redis_conn = await redis.init_pool_account_redis()
    redis.redis = redis.RedisStorage(redis_conn)


def shutdown_redis():
    redis.redis.close()


async def create_account(
        username: str,
        password: str,
        first_name: str,
        last_name: str) -> Employee:
    hashed_password = hashlib.sha1(password.encode()).hexdigest()
    account = await Employee.create(
        first_name=first_name,
        last_name=last_name,
        login=username,
        password=hashed_password
    )
    await redis.redis.set_account(username, hashed_password)
    return account


async def make_db_account_redis():
    employees = await Employee.all()
    for employee in employees:
        await redis.redis.set_account(employee.username, employee.password)
