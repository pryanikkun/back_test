import pytest

from .constants import (
    STATUS_401,
    STATUS_200,
    STATUS_201,
    CLIENT_DATA,
    FIRST_TICKET
)


def test_clients_get(client_app):
    response = client_app.get("/fox-ticket/clients/clients")
    assert response.status_code == STATUS_200
    assert response.json() == CLIENT_DATA
