# Standards

How we write and structure code in this repository.

---

## Principles

- Prefer clarity over cleverness
- Keep changes focused and reviewable
- Match existing patterns in the codebase once they exist
- Document decisions that affect other contributors

---

## Architecture

`frontend/`, `backend/`, and `agent/` use **Clean Architecture**. Dependencies point inward:

| Layer | Responsibility |
|-------|----------------|
| `domain/` | Entities, value objects, ports — no framework imports |
| `application/` | Use cases / interactors |
| `infrastructure/` | DB, HTTP clients, LangChain/OpenRouter, SQLite |
| `presentation/` | FastAPI routers, Next.js UI, agent entrypoints |

```
presentation → application → domain
infrastructure → application / domain
```

- Backend: `backend/src/backend/{domain,application,infrastructure,presentation}/`
- Agent: `agent/src/agent/{domain,application,infrastructure,presentation}/`
- Frontend: `frontend/src/{domain,application,infrastructure,presentation}/`; `frontend/src/app/` is a thin Next.js shell

`e2e/`, `data/`, and `lab/` are outside this layout.

---

## Lint & types

### Python (`backend/`, `agent/`)

| Tool | Role |
|------|------|
| **Ruff** | Lint with pycodestyle (`E`/`W`), bugbear (`B`), simplify (`SIM`) |
| **Bandit** | Security lint |
| **Pylint** | Additional static analysis |
| **Pyright** | Types |

### TypeScript (`frontend/`, `e2e/`)

| Tool | Role |
|------|------|
| **ESLint** + **SonarJS** | Lint / code smells |
| **`tsc`** | Types |

Fix lint/type errors before committing; do not bypass the hook.

---

## Testing

- Follow TDD in `docs/PROCESS.md`: exit criteria → unit test → implement → integration → e2e
- **pytest** — unit/integration in `backend/tests/`, `agent/tests/`
- **Vitest** — unit/integration in `frontend/tests/`
- E2E — Playwright in `e2e/`
- Never invoke a real model in tests—stubs only; mock APIs or use MSW
- Maintain **≥ 80%** coverage on product packages (`backend/`, `frontend/`, `agent/`)
- Experiments stay in `lab/`, not production paths

---

## Git hooks (Husky)

Pre-commit runs before every commit:

1. Lint — Ruff (pycodestyle, bugbear, simplify) + Bandit + Pylint + ESLint (SonarJS)
2. Types — Pyright + `tsc`
3. Coverage gate — pytest + Vitest must keep **≥ 80%**
4. E2E — Playwright (`e2e/`)

Commits fail if any step fails. Pre-commit is intentionally slow while E2E is on the hook.

---

## Naming

_To be defined._

---

## Documentation

- Keep product intent in `docs/SPEC.md`
- Keep working agreements in this file
- Update `docs/STATUS.md` when the project stage changes
