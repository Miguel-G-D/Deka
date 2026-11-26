"""Repository ports for clients and processes."""

from typing import Protocol

from backend.domain.client import Client
from backend.domain.process import Process


class ClientRepository(Protocol):
    def list_all(self) -> list[Client]: ...

    def get(self, client_id: str) -> Client | None: ...


class ProcessRepository(Protocol):
    def list_all(self) -> list[Process]: ...
