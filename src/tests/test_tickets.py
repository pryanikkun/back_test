import pytest

from .constants import (
    STATUS_401,
    STATUS_200,
    STATUS_201,
    FIRST_TICKET
)


def test_one_ticket_get(client_app):
    response = client_app.get("/fox-ticket/tickets/ticket/1")

    assert response.status_code == STATUS_200
    assert response.json() == FIRST_TICKET
