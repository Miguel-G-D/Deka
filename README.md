# Deka

Platform that helps bars and cafés manage reservations through an AI agent.

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js + shadcn/ui (`frontend/`) |
| Backend | FastAPI + SQLite (`backend/`) |
| Agent | LangChain + OpenRouter (`agent/`) |
| E2E | Playwright (`e2e/`) |

`frontend/`, `backend/`, and `agent/` follow Clean Architecture (`domain` → `application` ← `infrastructure` / `presentation`).

## Setup

```bash
uv sync --group dev
npm install
npx playwright install chromium
```

Requires Node ≥ 20 and [uv](https://docs.astral.sh/uv/). Initialize git before relying on Husky hooks (`npm prepare` / `npx husky`).

## Commands

```bash
npm run dev      # frontend :3000 + backend :8000
npm run check    # pytest + Vitest + Playwright (parallel)
npm run lint
npm run typecheck
```

E2E boots Next on `:3100` so it does not clash with `npm run dev` on `:3000`.

## Docs

See `AGENTS.md` and `docs/`.
