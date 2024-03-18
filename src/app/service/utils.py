from fastapi import HTTPException
import requests

from .. import redis
from ..models import Employee
from ..config import settings


def check_bot_access():
    """ Проверка подключения к боту """
    r2 = requests.get(f'https://api.telegram.org/bot{settings.TG_API}/setWebhook?url={settings.TG_ACCESS_URL}/fox-ticket/')
    if r2.json()['ok']:
        pass
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Проблемы с подключением к боту (проверьте/обновите URL в .env)"
        )


async def startup_redis():
    """ Установление соединения с redis """
    redis_conn = await redis.init_pool_account_redis()
    redis.redis = redis.RedisStorage(redis_conn)


def shutdown_redis():
    """ Закрытие соединения с redis """
    redis.redis.close()


async def make_db_account_redis():
    """ Заполнение БД redis """
    employees = await Employee.all()
    for employee in employees:
        await redis.redis.set_account(employee.username, employee.password)
