from ..models import Client, Ticket


async def create_client_if_not_exists(
        chat_id: int, first_name: str, username: str) -> Client:
    """ Находит клиента в БД, если не находит, то создаёт"""
    client = await Client.get_or_create(chat_id=chat_id,
                                        first_name=first_name,
                                        username=username)
    return client


async def check_ticket(chat_id: int, first_name: str, username: str) -> bool:
    """
    Проверка "можно ли открыть новый тикет" (TRUE - нет открытых, False-есть)
    :param chat_id:
    :param first_name: Имя клиента
    :param username: Ник клиента
    :return:
    """
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
            return True
    else:
        return True


async def get_open_ticket(
        chat_id: int, first_name: str, username: str) -> Ticket | None:
    """ Получаем тикет со статусом открыт/в процессе """
    client, some_bool = await create_client_if_not_exists(chat_id=chat_id,
                                                          first_name=first_name,
                                                          username=username)
    ticket = await Ticket.exists(client_id=client.id)
    if ticket:
        ticket_open = await Ticket.filter(status='OPEN', client_id=client.id).first()
        ticket_in_progress = await Ticket.filter(status='IN_PROGRESS', client_id=client.id).first()
        if ticket_open:
            return ticket_open
        elif ticket_in_progress:
            return ticket_in_progress
        else:
            return None
    else:
        return None



