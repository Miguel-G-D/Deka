# Plan

Active plan for Deka.

---

## Objective

Phase 2 continues in `lab/`: availability tool on mock calendar (after A1 menu agent), before Instagram or package promotion.

---

## Current focus

**A2 (lab):** Mock calendar + `check_availability` tool + availability evals. Done when notebook `lab/02_availability_v1.ipynb` runs with Groq key.

---

## Phase 2 checklist

- [x] A1 lab v1: menu data + `AgentResponse` + LangChain `create_agent` + Groq ToolStrategy evals (P/R) in `lab/`
- [x] A2 Mock calendar + availability fixtures / tool — unified in `lab/agent_v1.py` (+ notebooks 01/02)
- [ ] A3 Agenda-confirm conversation fixtures
- [ ] A4 Soft-reserve fixtures (confirm question + expect process update)
- [ ] B1 Promote agent into `agent/` package + formal tests
- [ ] B2 `check_availability` tool (mock calendar only — no real booking)
- [ ] B3 Soft reserve confirm + Process write API + dashboard refresh
- [ ] C Instagram simulator channel
- [x] D Meta Instagram adapter smoke (roles-only webhook + stub reply) — App Review still pending

### Notes

- Option B (adapter-first) for Instagram
- Meta smoke: `GET|POST /webhooks/meta`, stub `MessageHandler`, Graph `MessageSender`; env placeholders in `.env.example`
- No real calendar booking until the business process is known
- Lab notebooks are experiments; promote with TDD per `docs/PROCESS.md`
- A1/A2 auth: `GROQ_API_KEY` (fallback `OPENROUTER_API_KEY` if Groq key stored there)

---

## Phase 1 (dashboard) — done

Operator dashboard: Client 1—N Process, SQLite seeds, FastAPI → Next.js.

---

## Upcoming milestones

| Milestone | Outcome |
|-----------|---------|
| A1 lab menu agent | Precision/recall on product id |
| A2 lab availability | Tool + availability_accuracy evals |
| Soft reserve (lab → package) | Process updates |
| Instagram simulator → Meta | Channel adapter |
