from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import Command, CommandStart

from ..config import settings
from .utils import create_client_if_not_exists, check_ticket, get_open_ticket
from ..models import Ticket, Client, Message


tg_router = Router(name="fox-bot")
dp = Dispatcher()
bot = Bot(token=settings.TG_API)


@tg_router.message(CommandStart())
async def send_welcome(message: types.Message):
    """ Ответ на /start + добавление клиента в БД """
    client = await create_client_if_not_exists(chat_id=message.chat.id,
                                               first_name=message.chat.first_name,
                                               username=message.chat.username)
    await bot.send_message(chat_id=message.chat.id, text=
        f"Привет,{message.chat.first_name}, я тут \n"
        f"Список команд: \n"
        f"/start \n"
        f"/open_ticket \n"
        f"Напиши, что нужно"
    )


@tg_router.message(Command('open_ticket'))
async def open_ticket(message: types.Message):
    """ Открытие нового тикета """
    check = await check_ticket(chat_id=message.chat.id,
                               first_name=message.chat.first_name,
                               username=message.chat.username)
    if check:
        client = await Client.get(chat_id=message.chat.id)
        await Ticket.create(
            status="OPEN",
            client_id=client.id,
            employee_id_id=1
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Тикет открыт!")
    else:
        answer = "Пока обрабатывается предыдущий тикет "
        await bot.send_message(chat_id=message.chat.id, text=answer)

@tg_router.message()
async def message_ticket(message: types.Message):
    """ Обработка сообщения в открытом тикете """
    ticket = await get_open_ticket(chat_id=message.chat.id,
                                   first_name=message.chat.first_name,
                                   username=message.chat.username)

    if ticket:
        await Message.create(
            text=message.text,
            ticket_id=ticket.id
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Скоро мы с вами свяжемся :)")
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Напишите /open_ticket, чтобы открыть новый тикет")


dp.include_router(tg_router)
