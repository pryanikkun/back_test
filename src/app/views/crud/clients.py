from fastapi import APIRouter, Response, status, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from ...models import Client
from ..schemas import Client_Pydantic, Status

clients = APIRouter(
    prefix="/clients",
    tags=["clients"]
)


@clients.get('/clients')
async def get_clients():
    return await Client_Pydantic.from_queryset(Client.all())

