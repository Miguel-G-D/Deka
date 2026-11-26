"""Process (reservation conversation) domain model."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ProcessStatus(StrEnum):
    INTERESTED = "interested"
    RESERVED = "reserved"
    CONFIRMED = "confirmed"


class SpaceType(StrEnum):
    TERRACE = "terrace"
    BIRTHDAY = "birthday"
    TABLE = "table"


@dataclass(frozen=True, slots=True)
class Process:
    id: str
    client_id: str
    status: ProcessStatus
    party_size: int
    space_type: SpaceType
    received_at: datetime
    needs_human: bool

    def is_confirmed(self) -> bool:
        return self.status == ProcessStatus.CONFIRMED
