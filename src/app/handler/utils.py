from ..models import Client, Ticket


async def create_client_if_not_exists(
        chat_id: int, first_name: str, username: str):
    client = await Client.get_or_create(chat_id=chat_id,
                                        first_name=first_name,
                                        username=username)
    return client


async def check_ticket(chat_id: int, first_name: str, username: str, text: str):
    client, some_bool = await create_client_if_not_exists(chat_id=chat_id,
                                                          first_name=first_name,
                                                          username=username)
    ticket = await Ticket.exists(client_id=client.id)
    if ticket:
        tickets_opened = await Ticket.filter(status='OPEN').all()
        tickets_in_progress = await Ticket.filter(status='IN_PROGRESS').all()
        if tickets_opened or tickets_in_progress:
            return False
        else:
            await Ticket.create(
                text=text,
                status="OPEN",
                client_id=client.id,
                employee_id_id=1
            )
            return True
    else:
        await Ticket.create(
            text=text,
            status="OPEN",
            client_id=client.id,
            employee_id=1
        )
        return True
