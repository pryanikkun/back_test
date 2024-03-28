from fastapi import APIRouter, Response, status, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from ...dependency import login_required

from ...models import Client
from ..schemas import Client_Pydantic, Status

clients = APIRouter(
    prefix="/clients",
    tags=["clients"])
#     ,
#     dependencies=[Depends(login_required), ]
# )


@clients.get('/clients')
async def get_clients():
    """ Получение списка клиентов """
    return await Client_Pydantic.from_queryset(Client.all())

