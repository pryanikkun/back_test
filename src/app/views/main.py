import types
from fastapi import FastAPI, APIRouter, Depends
from aiogram import types

from ..dependency import login_required
from .crud import clients_router, tickets_router, employees_router
from ..handler.bot import dp, bot


def setup_views(api: FastAPI):
    api_router = APIRouter(
        prefix="/fox-ticket",
        dependencies=[Depends(login_required), ]
    )

    @api_router.post('/')
    async def tg_new_message(update: dict):
        print(update)
        update = types.Update(**update)
        await dp._process_update(bot=bot, update=update)

    api_router.include_router(tickets_router)
    api_router.include_router(clients_router)
    api_router.include_router(employees_router)
    api.include_router(api_router)


