from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum


class StatesOfTicket(Enum):
    """Этапы диалога с ботом"""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class Client(models.Model):
    chat_id = fields.BigIntField(index=True, description="Telegram chat ID")
    first_name = fields.CharField(null=True,
                                  max_length=30,
                                  description='First name')
    username = fields.CharField(max_length=64, description='Telegram username')
    tickets: fields.ReverseRelation['Ticket']

    class PydanticMeta:
        backward_relations = False


class Employee(models.Model):
    username = fields.CharField(index=True,
                                max_length=64,
                                unique=True,
                                description='Employee username')
    password = fields.CharField(max_length=64, description='Password')
    first_name = fields.CharField(null=True,
                                  max_length=30,
                                  description='First name')
    last_name = fields.CharField(null=True,
                                 max_length=30,
                                 description='Last name')
    tickets: fields.ReverseRelation['Ticket']


class Ticket(models.Model):
    status = fields.CharEnumField(
        enum_type=StatesOfTicket, description='Status ticket')
    ticket_date = fields.DatetimeField(
        auto_now_add=True, description='Date of creation/updating')
    client: fields.ForeignKeyNullableRelation[Client] = fields.ForeignKeyField(
        'models.Client', related_name='tickets', null=True, on_delete=fields.SET_NULL
    )
    employee = fields.ForeignKeyField(
        'models.Employee', related_name='tickets', null=True, on_delete=fields.SET_NULL
    )
    messages: fields.ReverseRelation['Message']


class Message(models.Model):
    text = fields.TextField(null=True, description="Messsage ticket")
    ticket = fields.ForeignKeyField(
        'models.Ticket', related_name='messages', null=True, on_delete=fields.SET_NULL
    )
