from fastapi import APIRouter, Response, status, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from ...handler.bot import bot

from ...models import Ticket, Client
from ..schemas import Ticket_Pydantic, TicketPost_Pydantic, Status, \
    UpdateTicket

tickets = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)


@tickets.get("", response_model=list[Ticket_Pydantic])
async def get_tickets(status: str = None,
                      employee_id: int = None,
                      date_asc: bool = False):
    if status and employee_id and date_asc:
        return await Ticket.filter(
            status=status,
            employee_id=employee_id
        ).order_by("ticket_date")
    elif employee_id and status: #посмотреть разницу
        return await Ticket.filter(status=status, employee_id=employee_id).all()
    elif status:
        return await Ticket.filter(status=status).all()
    elif employee_id:
        return await Ticket.filter(employee_id=employee_id).all()
    elif date_asc:
        return await Ticket_Pydantic.from_queryset(
            Ticket.all().order_by("ticket_date"))
    else:
        return await Ticket_Pydantic.from_queryset(
            Ticket.all().order_by("-ticket_date")
        )


@tickets.get('/ticket/{ticket_id}')
async def get_one_ticket(ticket_id: int):
    return await Ticket_Pydantic.from_queryset(Ticket.filter(id=ticket_id).all())


@tickets.put('/{ticket_id}',
             response_model=UpdateTicket,
             responses={404: {"model": HTTPNotFoundError}})
async def change_ticket_info(ticket_id: int,
                             ticket: UpdateTicket):
    ticket_obj = await Ticket.get_or_none(id=ticket_id)
    if ticket_obj:
        ticket_obj = await Ticket.update_from_dict(
            ticket_obj,
            data={
                "status": ticket.status,
                "employee_id": ticket.employee_id,
                "ticket_date": ticket.ticket_date
            }
        )
        await ticket_obj.save()
        client = await Client.get(id=ticket_obj.client_id)
        await bot.send_message(chat_id=client.chat_id,
                               text=f"Статус тикета изменился! "
                                    f"Статус: '{ticket.status}'")

        return {"status": ticket.status,
                "employee_id": ticket.employee_id,
                "ticket_date": ticket.ticket_date}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Тикета с id {ticket_id} нет"
        )


@tickets.delete('/{ticket_id}',
                response_model=Status,
                responses={404: {"model": HTTPNotFoundError}})
async def del_ticket(ticket_id: int,response: Response):
    ticket_obj = await Ticket.get_or_none(id=ticket_id)
    await ticket_obj.delete()
    response.status_code = status.HTTP_202_ACCEPTED
    return Status(message=f"Deleted ticket {ticket_id}")
