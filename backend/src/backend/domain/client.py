"""Client (diner) domain model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Client:
    id: str
    name: str
    phone: str
