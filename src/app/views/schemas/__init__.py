from pydantic import BaseModel
from ...models import Client, Employee, Ticket, Message
from tortoise.contrib.pydantic import pydantic_model_creator

Client_Pydantic = pydantic_model_creator(Client, name='Client')
Employee_Pydantic = pydantic_model_creator(Employee, name='Employee')
EmployeePost_Pydantic = pydantic_model_creator(Employee, name='Employee',
                                               exclude_readonly=True)
Ticket_Pydantic = pydantic_model_creator(Ticket, name='Ticket')
TicketPost_Pydantic = pydantic_model_creator(Ticket, name='TicketPost',
                                             exclude_readonly=True)

Message_Pydantic = pydantic_model_creator(Message, name='Message')
MessagePost_Pydantic = pydantic_model_creator(Message, name='Message',
                                              exclude_readonly=True)


class Status(BaseModel):
    message: str


class UpdateTicket(BaseModel):
    status: str
    employee_id: int | None


class SendMessage(BaseModel):
    text: str
    ticket_id: int


class UpdateEmployee(BaseModel):
    username: str
    first_name: str
    last_name: str
