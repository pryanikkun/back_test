import datetime

from pydantic import BaseModel
from ...models import Client, Employee, Ticket
from tortoise.contrib.pydantic import pydantic_model_creator

Client_Pydantic = pydantic_model_creator(Client, name='Client')
Employee_Pydantic = pydantic_model_creator(Employee, name='Employee')
EmployeePost_Pydantic = pydantic_model_creator(Employee, name='Employee',
                                               exclude_readonly=True)
Ticket_Pydantic = pydantic_model_creator(Ticket, name='Ticket')
TicketPost_Pydantic = pydantic_model_creator(Ticket, name='TicketPost',
                                             exclude_readonly=True)


class Status(BaseModel):
    message: str


class UpdateTicket(BaseModel):
    status: str
    employee_id: int | None
    ticket_date: datetime.datetime = datetime.datetime.now()
