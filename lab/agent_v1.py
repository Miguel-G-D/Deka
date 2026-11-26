"""Lab unified 8onzas agent: menu + hours + availability (two-phase ReAct + structured)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
VENUE_DIR = DATA_DIR / "venue"
MENU_CASES_PATH = DATA_DIR / "tests" / "menu_cases.json"
AVAIL_CASES_PATH = DATA_DIR / "tests" / "availability_cases.json"
CALENDAR_PATH = VENUE_DIR / "8onzas-calendar.json"

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

_WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


class DayHours(BaseModel):
    open: str
    close: str


class VenueProfile(BaseModel):
    venue_id: str
    name: str
    assistant_name: str
    greeting: str
    timezone: str
    hours: dict[str, DayHours | None]
    spaces: list[str]
    reservation_rules: dict[str, int]


class MenuItem(BaseModel):
    id: str
    name: str
    description: str = ""
    price: float
    tags: list[str] = Field(default_factory=list)


class MenuCategory(BaseModel):
    id: str
    name: str
    items: list[MenuItem]


class Menu(BaseModel):
    venue_id: str
    currency: str = "ARS"
    categories: list[MenuCategory]


class CalendarBooking(BaseModel):
    date: str
    time: str
    space: str
    party_size: int


class VenueCalendar(BaseModel):
    venue_id: str
    timezone: str
    slot_minutes: int = 90
    capacity: dict[str, int]
    bookings: list[CalendarBooking] = Field(default_factory=list)


class ProductRef(BaseModel):
    found: bool = Field(description="True si el ítem está en el menú; false si no existe")
    id: str | None = Field(
        default=None,
        description="Id exacto del menú (ej. latte, bowl-vegano); null si not found",
    )
    name: str | None = Field(default=None, description="Nombre del producto; null si not found")
    price: float | None = Field(default=None, description="Precio numérico del MENÚ; null si not found")
    currency: str | None = Field(default="ARS", description="Moneda, normalmente ARS")


class HoursRef(BaseModel):
    day: str | None = Field(
        default=None,
        description="Día consultado en inglés lowercase (monday..sunday)",
    )
    open: str | None = Field(default=None, description="Hora de apertura HH:MM")
    close: str | None = Field(default=None, description="Hora de cierre HH:MM")


class AvailabilityRef(BaseModel):
    checked: bool = Field(description="True si se consultó disponibilidad (tool)")
    available: bool | None = Field(
        default=None,
        description="True si hay lugar; false si no; null si no se checó",
    )
    date: str | None = Field(default=None, description="Fecha ISO YYYY-MM-DD")
    time: str | None = Field(default=None, description="Hora HH:MM")
    party_size: int | None = Field(default=None, description="Cantidad de personas")
    space: str | None = Field(default=None, description="Espacio: table|terrace|birthday")
    reason: str | None = Field(default=None, description="Motivo breve si no disponible")


class AgentResponse(BaseModel):
    message: str = Field(description="Respuesta en lenguaje natural al usuario (español)")
    intent: Literal["menu", "hours", "unknown_item", "availability", "other"] = Field(
        description="Clasificación de la consulta",
    )
    product: ProductRef | None = Field(
        default=None,
        description="Datos del producto si intent es menu o unknown_item; null si no aplica",
    )
    hours: HoursRef | None = Field(
        default=None,
        description="Horario si intent es hours; null si no aplica",
    )
    availability: AvailabilityRef | None = Field(
        default=None,
        description="Resultado de disponibilidad si intent es availability; null si no aplica",
    )


class MenuExpect(BaseModel):
    product_id: str | None = None
    product_found: bool = True
    price: float | None = None
    currency: str | None = None
    day: str | None = None
    open: str | None = None
    close: str | None = None
    must_mention: list[str] = Field(default_factory=list)
    must_not_mention: list[str] = Field(default_factory=list)


class MenuCase(BaseModel):
    id: str
    capability: Literal["menu", "hours", "unknown_item"]
    user: str
    expect: MenuExpect


class MenuCaseSuite(BaseModel):
    venue_id: str = "8onzas"
    cases: list[MenuCase]


class AvailabilityExpect(BaseModel):
    available: bool
    date: str | None = None
    time: str | None = None
    party_size: int | None = None
    space: str | None = None
    must_mention: list[str] = Field(default_factory=list)
    must_not_mention: list[str] = Field(default_factory=list)


class AvailabilityCase(BaseModel):
    id: str
    capability: Literal["availability"]
    user: str
    expect: AvailabilityExpect


class AvailabilityCaseSuite(BaseModel):
    venue_id: str = "8onzas"
    cases: list[AvailabilityCase]


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from repo .env without overriding existing env."""
    target = path or (REPO_ROOT / ".env")
    if not target.exists():
        return
    for raw in target.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def resolve_groq_api_key(api_key: str | None = None) -> str:
    load_dotenv()
    key = (
        api_key
        or os.environ.get("GROQ_API_KEY")
        or os.environ.get("OPENROUTER_API_KEY")
    )
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is required (fallback: OPENROUTER_API_KEY if you "
            "already stored the Groq key under that name)."
        )
    return key


def load_profile(path: Path | None = None) -> VenueProfile:
    target = path or (VENUE_DIR / "8onzas-profile.json")
    return VenueProfile.model_validate_json(target.read_text(encoding="utf-8"))


def load_menu(path: Path | None = None) -> Menu:
    target = path or (VENUE_DIR / "8onzas-menu.json")
    return Menu.model_validate_json(target.read_text(encoding="utf-8"))


def load_calendar(path: Path | None = None) -> VenueCalendar:
    target = path or CALENDAR_PATH
    return VenueCalendar.model_validate_json(target.read_text(encoding="utf-8"))


def load_cases(path: Path | None = None) -> MenuCaseSuite:
    target = path or MENU_CASES_PATH
    return MenuCaseSuite.model_validate_json(target.read_text(encoding="utf-8"))


def load_availability_cases(path: Path | None = None) -> AvailabilityCaseSuite:
    target = path or AVAIL_CASES_PATH
    return AvailabilityCaseSuite.model_validate_json(target.read_text(encoding="utf-8"))


def _parse_hhmm(value: str) -> tuple[int, int]:
    hour_s, minute_s = value.split(":")
    return int(hour_s), int(minute_s)


def _within_hours(open_hhmm: str, close_hhmm: str, time_hhmm: str) -> bool:
    open_t = _parse_hhmm(open_hhmm)
    close_t = _parse_hhmm(close_hhmm)
    slot_t = _parse_hhmm(time_hhmm)
    return open_t <= slot_t < close_t


def compute_availability(
    *,
    date: str,
    time: str,
    party_size: int,
    space: str = "table",
    calendar: VenueCalendar | None = None,
    profile: VenueProfile | None = None,
) -> dict[str, Any]:
    """Pure availability check against mock calendar + profile rules."""
    calendar = calendar or load_calendar()
    profile = profile or load_profile()

    base: dict[str, Any] = {
        "available": False,
        "reason": None,
        "capacity": None,
        "busy": 0,
        "space": space,
        "date": date,
        "time": time,
        "party_size": party_size,
    }

    min_size = profile.reservation_rules.get("min_party_size", 1)
    max_size = profile.reservation_rules.get("max_party_size", 12)
    if party_size < min_size or party_size > max_size:
        base["reason"] = (
            f"party_size {party_size} fuera de rango ({min_size}-{max_size})"
        )
        return base

    if space not in calendar.capacity:
        base["reason"] = f"espacio desconocido: {space}"
        return base

    try:
        day = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        base["reason"] = "fecha inválida; usar YYYY-MM-DD"
        return base

    weekday = _WEEKDAYS[day.weekday()]
    day_hours = profile.hours.get(weekday)
    if day_hours is None:
        base["reason"] = f"cerrado ({weekday})"
        return base

    if not _within_hours(day_hours.open, day_hours.close, time):
        base["reason"] = f"fuera de horario ({day_hours.open}-{day_hours.close})"
        return base

    capacity = calendar.capacity[space]
    busy = sum(
        b.party_size
        for b in calendar.bookings
        if b.date == date and b.time == time and b.space == space
    )
    remaining = capacity - busy
    available = party_size <= remaining
    base.update(
        {
            "available": available,
            "capacity": capacity,
            "busy": busy,
            "reason": None if available else "sin capacidad en ese slot",
        }
    )
    return base


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TIME_RE = re.compile(r"^\d{2}:\d{2}$")


def _validate_availability_args(
    date: str,
    time: str,
    party_size: int,
    space: str,
    *,
    allowed_spaces: list[str],
) -> None:
    """Raise ValueError with actionable message; becomes ToolMessage in the ReAct loop."""
    if not isinstance(date, str) or not _DATE_RE.match(date):
        raise ValueError("date debe ser string ISO YYYY-MM-DD (ej. 2026-11-28)")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"date inválida: {date}") from exc

    if not isinstance(time, str) or not _TIME_RE.match(time):
        raise ValueError("time debe ser HH:MM en 24h (ej. 20:00)")
    hour, minute = time.split(":")
    if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
        raise ValueError(f"time fuera de rango: {time}")

    if not isinstance(party_size, int) or isinstance(party_size, bool):
        raise ValueError("party_size debe ser un entero")
    if party_size < 1:
        raise ValueError("party_size debe ser >= 1")

    if space not in allowed_spaces:
        raise ValueError(
            f"space inválido: {space!r}. Usá uno de: {', '.join(allowed_spaces)}"
        )


def make_check_availability_tool(
    calendar: VenueCalendar | None = None,
    profile: VenueProfile | None = None,
):
    """Bind calendar/profile into a LangChain tool for create_agent."""
    cal = calendar or load_calendar()
    prof = profile or load_profile()
    allowed_spaces = list(prof.spaces)

    @tool
    def check_availability(
        date: str,
        time: str,
        party_size: int,
        space: str = "table",
    ) -> dict[str, Any]:
        """Consulta disponibilidad mock de 8onzas para una fecha/hora/espacio.

        Args:
            date: Fecha ISO YYYY-MM-DD.
            time: Hora HH:MM (24h).
            party_size: Cantidad de personas.
            space: table, terrace o birthday.
        """
        _validate_availability_args(
            date,
            time,
            party_size,
            space,
            allowed_spaces=allowed_spaces,
        )
        return compute_availability(
            date=date,
            time=time,
            party_size=party_size,
            space=space,
            calendar=cal,
            profile=prof,
        )

    return check_availability


def build_system_prompt(
    profile: VenueProfile,
    menu: Menu,
    calendar: VenueCalendar,
) -> str:
    profile_json = json.dumps(profile.model_dump(), ensure_ascii=False, indent=2)
    menu_json = json.dumps(menu.model_dump(), ensure_ascii=False, indent=2)
    calendar_json = json.dumps(calendar.model_dump(), ensure_ascii=False, indent=2)
    return f"""Sos el {profile.assistant_name} del café {profile.name} (Argentina).

Capacidades:
- Menú: platos, precios, tags (ej. vegano). Precios SOLO del JSON de menú ({menu.currency}).
- Horario: apertura/cierre por día del perfil.
- Disponibilidad de mesas: SOLO vía la tool check_availability (no inventes slots).
- Si preguntan por un producto que NO está en el menú: product.found=false.

Reglas:
- Contestá en español, tono claro y hospitalario.
- Ids de producto exactos del menú (ej. latte, bowl-vegano).
- La ÚNICA tool disponible es check_availability. No inventes otras tools.
- Para disponibilidad / reserva / mesa para N en fecha+hora: llamá check_availability
  cuando haga falta; si la tool devuelve error, corregí los args y reintentá.
- Después de usar tools (si aplica), respondé en texto claro al usuario con los datos
  (precios del menú, horario, o resultado de disponibilidad). Un paso posterior empaqueta
  eso en AgentResponse; vos enfocáte en tools + respuesta útil.
- Espacios válidos: {", ".join(profile.spaces)}.
- Aún NO confirmes reservas blandas ni escribas en agenda (solo informar disponibilidad).

PERFIL:
{profile_json}

MENÚ:
{menu_json}

CALENDARIO_MOCK (la tool ya aplica capacidad/bookings; no copies a mano):
{calendar_json}
"""


_PHASE2_PACK_PROMPT = """Empaquetá la conversación anterior en un AgentResponse válido.
Usá SOLO hechos del historial (mensajes del asistente y resultados de check_availability).
Reglas:
- intent: menu | hours | unknown_item | availability | other
- product / hours / availability: null si no aplican
- Si hubo check_availability exitoso: availability.checked=true y copiá available/date/time/party_size/space/reason del tool result
- message: respuesta en español al usuario (podés basarte en el último mensaje del asistente)
No inventes tools ni datos que no estén en el historial.
"""


@dataclass(frozen=True)
class AgentBundle:
    """Two-phase agent: ReAct graph (tools) + structured packer (no tools)."""

    react: Any
    structured: Any


def _build_chat_openai(
    *,
    model: str,
    api_key: str,
) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=GROQ_BASE_URL,
        temperature=0,
        timeout=120,
        max_retries=5,
        max_tokens=1024,
    )


def build_agent(
    profile: VenueProfile | None = None,
    menu: Menu | None = None,
    calendar: VenueCalendar | None = None,
    *,
    model: str = DEFAULT_GROQ_MODEL,
    api_key: str | None = None,
) -> AgentBundle:
    """Build two-phase agent (Groq-safe): tools XOR structured output per request.

    Phase 1 — ReAct create_agent with check_availability only (no response_format).
    Phase 2 — separate LLM call with_structured_output(AgentResponse), no tools.
    """
    profile = profile or load_profile()
    menu = menu or load_menu()
    calendar = calendar or load_calendar()
    key = resolve_groq_api_key(api_key)
    check_availability = make_check_availability_tool(calendar, profile)

    react_llm = _build_chat_openai(model=model, api_key=key)
    react = create_agent(
        model=react_llm,
        tools=[check_availability],
        system_prompt=build_system_prompt(profile, menu, calendar),
        name="8onzas-agent-v1-react",
    )

    pack_llm = _build_chat_openai(model=model, api_key=key)
    # json_schema without tools — Groq allows this; not combined with function calling.
    structured = pack_llm.with_structured_output(AgentResponse, method="json_schema")

    return AgentBundle(react=react, structured=structured)


def _parse_agent_response_text(content: str) -> AgentResponse | None:
    text = content.strip()
    if not text:
        return None
    candidates: list[str] = [text]
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        candidates.insert(0, fence.group(1).strip())
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start : end + 1])
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            return AgentResponse.model_validate_json(candidate)
        except ValueError:
            continue
    return None


def _extract_response(result: Any) -> AgentResponse:
    if isinstance(result, AgentResponse):
        return result
    if isinstance(result, dict):
        structured = result.get("structured_response")
        if isinstance(structured, AgentResponse):
            return structured
        if isinstance(structured, dict):
            return AgentResponse.model_validate(structured)
        messages = result.get("messages") or []
        for message in reversed(messages):
            content = getattr(message, "content", None)
            if isinstance(content, str):
                parsed = _parse_agent_response_text(content)
                if parsed is not None:
                    return parsed
            if isinstance(content, list):
                parts = [
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                ]
                parsed = _parse_agent_response_text("\n".join(p for p in parts if p))
                if parsed is not None:
                    return parsed
    raise ValueError(f"Could not extract AgentResponse from result: {type(result)}")


def _resolve_bundle(agent: Any | None) -> AgentBundle:
    if agent is None:
        return build_agent()
    if isinstance(agent, AgentBundle):
        return agent
    raise TypeError(
        "agent must be an AgentBundle from build_agent() "
        f"(got {type(agent).__name__})"
    )


def _had_availability_tool_success(messages: list[Any]) -> bool:
    for message in messages:
        if not isinstance(message, ToolMessage):
            continue
        name = getattr(message, "name", None) or ""
        if name != "check_availability":
            continue
        status = getattr(message, "status", "success")
        if status == "error":
            continue
        return True
    return False


def _pack_structured(
    structured: Any,
    messages: list[Any],
    *,
    repair_hint: str | None = None,
) -> AgentResponse:
    pack_msgs: list[Any] = [SystemMessage(content=_PHASE2_PACK_PROMPT), *messages]
    if repair_hint:
        pack_msgs.append(
            HumanMessage(
                content=(
                    "El empaquetado anterior falló la validación. "
                    f"Corregí el AgentResponse. Detalle: {repair_hint}"
                )
            )
        )
    raw = structured.invoke(pack_msgs)
    if isinstance(raw, AgentResponse):
        return raw
    if isinstance(raw, dict):
        return AgentResponse.model_validate(raw)
    raise ValueError(f"Structured packer returned unexpected type: {type(raw)}")


def invoke_agent(user: str, agent: Any | None = None) -> AgentResponse:
    """Phase 1 ReAct (tools) then Phase 2 structured pack (no tools)."""
    bundle = _resolve_bundle(agent)

    # --- Phase 1: tools only (Groq) ---
    try:
        state = bundle.react.invoke(
            {"messages": [{"role": "user", "content": user}]},
        )
    except Exception as exc:
        raise RuntimeError(f"phase1_react_failed: {type(exc).__name__}: {exc}") from exc

    if not isinstance(state, dict) or "messages" not in state:
        raise RuntimeError("phase1_react_failed: missing messages in agent state")
    messages = list(state["messages"])

    # Soft gate: availability questions should have used the tool when possible.
    # We still run phase 2 so evals can record checked=false / wrong available.
    _ = _had_availability_tool_success(messages)

    # --- Phase 2: structured output only (no tools) ---
    try:
        return _pack_structured(bundle.structured, messages)
    except Exception as first_exc:
        hint = f"{type(first_exc).__name__}: {first_exc}"
        try:
            return _pack_structured(bundle.structured, messages, repair_hint=hint)
        except Exception as second_exc:
            # Last resort: parse any JSON left in phase-1 AI messages
            try:
                return _extract_response({"messages": messages})
            except Exception:
                raise RuntimeError(
                    f"phase2_structured_failed: {type(second_exc).__name__}: {second_exc}"
                ) from second_exc


def evaluate(
    suite: MenuCaseSuite | None = None,
    *,
    agent: Any | None = None,
) -> dict[str, Any]:
    """Menu/hours/unknown evals (precision/recall on product id)."""
    suite = suite or load_cases()
    graph = agent or build_agent()

    rows: list[dict[str, Any]] = []
    tp = fp = fn = 0
    unknown_ok = 0
    unknown_total = 0
    hours_ok = 0
    hours_total = 0

    for case in suite.cases:
        row: dict[str, Any] = {
            "id": case.id,
            "capability": case.capability,
            "expected_product_id": None,
            "predicted_product_id": None,
            "product_ok": False,
            "mention_ok": False,
            "intent": None,
            "message": None,
            "error": None,
        }
        try:
            response = invoke_agent(case.user, agent=graph)
        except Exception as exc:  # noqa: BLE001 — lab eval must not abort suite
            row["error"] = f"{type(exc).__name__}: {exc}"
            rows.append(row)
            continue

        predicted_id = response.product.id if response.product and response.product.found else None
        expected_id = case.expect.product_id if case.expect.product_found else None

        if expected_id is not None:
            if predicted_id == expected_id:
                tp += 1
                product_ok = True
            elif predicted_id is None:
                fn += 1
                product_ok = False
            else:
                fp += 1
                fn += 1
                product_ok = False
        elif predicted_id is not None:
            fp += 1
            product_ok = False
        else:
            product_ok = True

        if case.capability == "unknown_item":
            unknown_total += 1
            found = bool(response.product and response.product.found)
            if not found:
                unknown_ok += 1

        if case.capability == "hours":
            hours_total += 1
            hours = response.hours
            if (
                hours
                and hours.open == case.expect.open
                and hours.close == case.expect.close
            ):
                hours_ok += 1

        message_l = response.message.lower()
        mention_ok = all(m.lower() in message_l for m in case.expect.must_mention)
        not_mention_ok = all(
            m.lower() not in message_l for m in case.expect.must_not_mention
        )

        row.update(
            {
                "expected_product_id": expected_id,
                "predicted_product_id": predicted_id,
                "product_ok": product_ok,
                "mention_ok": mention_ok and not_mention_ok,
                "intent": response.intent,
                "message": response.message,
            }
        )
        rows.append(row)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "unknown_accuracy": (unknown_ok / unknown_total) if unknown_total else None,
        "hours_accuracy": (hours_ok / hours_total) if hours_total else None,
        "rows": rows,
    }


def evaluate_availability(
    suite: AvailabilityCaseSuite | None = None,
    *,
    agent: Any | None = None,
) -> dict[str, Any]:
    """Availability evals: accuracy / slot_match / tool_discipline."""
    suite = suite or load_availability_cases()
    graph = agent or build_agent()

    rows: list[dict[str, Any]] = []
    avail_ok = 0
    avail_total = 0
    slot_ok = 0
    slot_total = 0
    checked_ok = 0
    checked_total = 0

    for case in suite.cases:
        row: dict[str, Any] = {
            "id": case.id,
            "capability": case.capability,
            "expected_available": case.expect.available,
            "predicted_available": None,
            "availability_ok": False,
            "slot_ok": False,
            "checked": False,
            "intent": None,
            "message": None,
            "error": None,
        }
        try:
            response = invoke_agent(case.user, agent=graph)
        except Exception as exc:  # noqa: BLE001 — lab eval must not abort suite
            row["error"] = f"{type(exc).__name__}: {exc}"
            rows.append(row)
            continue

        avail = response.availability
        predicted = avail.available if avail is not None else None
        checked = bool(avail and avail.checked)

        avail_total += 1
        availability_ok = predicted is not None and predicted == case.expect.available
        if availability_ok:
            avail_ok += 1

        checked_total += 1
        if checked:
            checked_ok += 1

        slot_match = True
        if case.expect.date is not None:
            slot_total += 1
            slot_match = bool(avail and avail.date == case.expect.date)
            if case.expect.time is not None:
                slot_match = slot_match and bool(avail and avail.time == case.expect.time)
            if case.expect.party_size is not None:
                slot_match = slot_match and bool(
                    avail and avail.party_size == case.expect.party_size
                )
            if case.expect.space is not None:
                slot_match = slot_match and bool(avail and avail.space == case.expect.space)
            if slot_match:
                slot_ok += 1

        message_l = (response.message or "").lower()
        mention_ok = all(m.lower() in message_l for m in case.expect.must_mention)
        not_mention_ok = all(
            m.lower() not in message_l for m in case.expect.must_not_mention
        )

        row.update(
            {
                "predicted_available": predicted,
                "availability_ok": availability_ok,
                "slot_ok": slot_match,
                "checked": checked,
                "mention_ok": mention_ok and not_mention_ok,
                "intent": response.intent,
                "message": response.message,
            }
        )
        rows.append(row)

    return {
        "availability_accuracy": (avail_ok / avail_total) if avail_total else None,
        "slot_match": (slot_ok / slot_total) if slot_total else None,
        "tool_discipline": (checked_ok / checked_total) if checked_total else None,
        "avail_ok": avail_ok,
        "avail_total": avail_total,
        "slot_ok": slot_ok,
        "slot_total": slot_total,
        "checked_ok": checked_ok,
        "checked_total": checked_total,
        "rows": rows,
    }
