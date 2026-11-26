"""Dashboard view models."""

from dataclasses import dataclass

from backend.domain.process import ProcessStatus, SpaceType


@dataclass(frozen=True, slots=True)
class ActivityPoint:
    date: str
    count: int


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    total_processes: int
    interested_count: int
    reserved_count: int
    confirmed_count: int
    needs_human_count: int
    total_party_size: int
    activity_series: tuple[ActivityPoint, ...]


@dataclass(frozen=True, slots=True)
class ProcessRow:  # pylint: disable=too-many-instance-attributes
    process_id: str
    client_id: str
    client_name: str
    status: ProcessStatus
    party_size: int
    space_type: SpaceType
    received_at: str
    needs_human: bool
