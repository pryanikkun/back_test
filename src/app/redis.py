import asyncio_redis
from typing import Optional

from .config import settings


async def init_pool_account_redis():
    """ Создание пула в redis"""
    redis_connect = await asyncio_redis.Pool.create(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=1,
        poolsize=1)
    return redis_connect


class RedisStorage:
    def __init__(self, session):
        self.session = session

    async def set_account(self, key: str, value: str):
        """Сохранить объект в Redis
        :param key: Ключ
        :param value: Объект для сохранения"""
        await self.session.set(key, value)

    async def get_value(self, key: str):
        """Получить значение из Redis по ключу
        :param key: Ключ
        :return: значение объекта из Redis"""
        value = await self.session.get(key)
        if value is None:
            return None
        return value

    def close(self):
        """ Закрытие сессии """
        self.session.close()


redis: Optional[RedisStorage] = None
