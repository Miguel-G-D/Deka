"""Compatibility shim — unified agent lives in agent_v1.py."""

from agent_v1 import *  # noqa: F403
from agent_v1 import (  # noqa: F401
    AgentResponse,
    AvailabilityCase,
    AvailabilityCaseSuite,
    AvailabilityExpect,
    AvailabilityRef,
    VenueCalendar,
    build_agent,
    compute_availability,
    evaluate_availability,
    invoke_agent,
    load_availability_cases,
    load_calendar,
    make_check_availability_tool,
)
