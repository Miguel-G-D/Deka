# Process

Planning and ways of working for Deka.

---

## Working mode

1. Read `AGENTS.md` and the relevant docs in `docs/` before starting
2. Align with `docs/SPEC.md` and the current `docs/PLAN.md`
3. Keep scope tight; prefer small, complete increments
4. Update `docs/STATUS.md` when stage or next steps change

---

## Methodology (TDD)

Every feature follows this order. No implementation before a failing test that encodes the exit criteria.

### 1. Plan

- Take the feature from `docs/PLAN.md`
- Define **exit criteria** (what “done” means) before writing code
- Sketch the function/API contract only—no full implementation yet

### 2. Unit tests first (per package)

- Write unit tests that assert the exit criteria
- Each package owns its tests: `backend/tests/`, `frontend/tests/`, `agent/tests/`
- **Never call a real model** to run logic under test—use stubs only
- Mock or use **MSW** to simulate API requests; no live network

### 3. Implement until green

- Implement the minimum code that makes the unit tests pass
- Keep stubs/mocks for models and external APIs

### 4. UI → integration

- After the UI exists, add integration tests in that package’s `tests/` (e.g. `frontend/tests/integration/`)
- Same rule: stubs + MSW; no real model or live APIs

### 5. E2E (`e2e/`)

- Once the slice works end-to-end in the app, cover the critical path in `e2e/`
- Prefer user-visible flows tied to exit criteria in `PLAN.md`

```
PLAN exit criteria → unit test in package (fail) → implement → unit green
                 → UI → package integration → e2e/
```

---

## Planning

- Active plan: `docs/PLAN.md`
- Spec and goals: `docs/SPEC.md`
- Do not expand scope without updating the spec

---

## Reviews & delivery

- A change is ready when its exit criteria are covered by tests and the relevant suite is green
- Prefer small PRs that deliver one complete increment

---

## Experiments

- Prototypes and notebooks belong in `lab/`
- Promote into product folders only when ready
- Lab work does not skip TDD when promoted
