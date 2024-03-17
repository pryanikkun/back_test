from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import Command, CommandStart

from ..config import settings
from .utils import create_client_if_not_exists, check_ticket


tg_router = Router(name="fox-bot")
dp = Dispatcher()
bot = Bot(token=settings.TG_API)


@tg_router.message(CommandStart())
async def send_welcome(message: types.Message):
    client = await create_client_if_not_exists(chat_id=message.chat.id,
                                               first_name=message.chat.first_name,
                                               username=message.chat.username)
    await bot.send_message(chat_id=message.chat.id, text=
        f"Привет,{message.chat.first_name}, я тут \n"
        f"Список команд: \n"
        f"/start \n"
        f"/open-ticket \n"
        f"Напиши, что нужно"
    )


@tg_router.message(Command('/open-ticket'))
async def open_ticket(message: types.Message):
    """
    Открытие нового тикета
    :param message:  Message
    :return:
    """
    check = await check_ticket(chat_id=message.chat.id,
                               first_name=message.chat.first_name,
                               username=message.chat.username,
                               text=message.text)
    if check:
        await bot.send_message(chat_id=message.chat.id, text="Тикет открыт")
    else:
        answer = "Пока обрабатывается предыдущий тикет "
        await bot.send_message(chat_id=message.chat.id, text=answer)


dp.include_router(tg_router)
