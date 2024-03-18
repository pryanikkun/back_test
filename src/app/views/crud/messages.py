from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from ...dependency import login_required
from ...handler.bot import bot
from ...models import Message, Ticket, Client

from ..schemas import SendMessage, Message_Pydantic

messages = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(login_required), ]
)


@messages.get("")
async def get_messages(ticket_id: int = None):
    """ Получение сообщений """
    return await Message_Pydantic.from_queryset(
        Message.filter(ticket_id=ticket_id).all()
    )


@messages.post("",
               response_model=SendMessage,
               responses={404: {"model": HTTPNotFoundError}})
async def create_answer(message: SendMessage):
    """ Отправка сообщения в тикет """
    ticket_obj = await Ticket.get_or_none(id=message.ticket_id)
    client = await Client.get(id=ticket_obj.client_id)
    chat_id = client.chat_id
    text = message.text
    await bot.send_message(chat_id=chat_id, text=text)
    return {
        'ticket_id': message.ticket_id,
        'chat_id': chat_id,
        'text': text
    }
