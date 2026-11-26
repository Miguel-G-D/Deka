# Tech stack

Technologies used to build Deka.

---

## Overview

| Layer | Choice | Location |
|-------|--------|----------|
| Frontend | Next.js + shadcn/ui | `frontend/` |
| Backend | FastAPI + SQLite | `backend/` |
| Agent | LangChain `create_agent` + OpenRouter | `agent/` |
| Business data | Venue / ops reference for the model | `data/` |
| E2E | Playwright | `e2e/` |
| Experiments | Notebooks only | `lab/` |

---

## Frontend

- **Next.js** — UI and operator dashboard (Clean Architecture under `frontend/src/`)
- **shadcn/ui** — design-system components; map tokens from `docs/BRAND.md`

---

## Backend

- **FastAPI** — HTTP APIs and integrations (Clean Architecture under `backend/src/backend/`)
- **SQLite** — primary datastore for this stage

---

## Agent

- **LangChain** — agent via `create_agent` (Clean Architecture under `agent/src/agent/`)
- **OpenRouter** — model routing / LLM provider
- Stub models in tests; never call a real model from unit/integration suites

---

## Data

`data/` holds business reference content the agent uses (menus, hours, policies, venue facts)—not application runtime DB files.

---

## Testing & tooling

| Area | Location | Tooling |
|------|----------|---------|
| Unit / integration (Python) | `backend/tests/`, `agent/tests/` | pytest; stubs / mocks; **≥ 80%** coverage |
| Unit / integration (TS) | `frontend/tests/` | Vitest; stubs / MSW; **≥ 80%** coverage |
| E2E | `e2e/` | Playwright — critical cross-package flows |
| Lint (Python) | `backend/`, `agent/` | Ruff (`E`/`W` pycodestyle, `B` bugbear, `SIM` simplify) · Bandit · Pylint |
| Lint (TS) | `frontend/`, `e2e/` | ESLint + SonarJS |
| Types | Python / TS | Pyright · `tsc` |
| Git hooks | repo root | Husky pre-commit: lint → types → coverage → e2e |
| Experiments | `lab/` | Promote into packages only with TDD |
