# Status

Current project stage and next steps.

---

## Current stage

Phase 2 / **A2 lab** + **D Meta adapter smoke** in backend (`/webhooks/meta`, stub reply). Soft-reserve, agent promote, and App Review still pending.

---

## Done

- Phase 1 dashboard (SQLite seeds, APIs, UI, e2e)
- A1 data: `data/venue/8onzas-profile.json`, `8onzas-menu.json`, `data/tests/menu_cases.json`
- A1/A2 lab: `lab/agent_v1.py` (single agent) + `01_menu_agent_v1.ipynb` / `02_availability_v1.ipynb`
- A2 data: `data/venue/8onzas-calendar.json`, `data/tests/availability_cases.json`
- Shims: `menu_agent_v1.py` / `availability_agent_v1.py` re-export `agent_v1`
- D smoke: Meta webhook adapter (verify + HMAC + stub echo via Graph), `.env.example` `META_*` placeholders
- Public legal pages for Meta App settings: `/privacy` (incl. `#data-deletion`) and `/terms` in the Next.js frontend

---

## Next

- Run `02_availability_v1.ipynb` evals and record availability_accuracy / slot_match / tool_discipline
- A3 agenda-confirm fixtures
- Manual Meta smoke (roles-only + HTTPS tunnel) — see checklist below
- After frontend HTTPS deploy, paste into Meta: `https://<host>/privacy`, `https://<host>/terms` (deletion instructions: `…/privacy#data-deletion`)
- Later: swap `StubEchoHandler` → agent `MessageHandler`; IG simulator; App Review

---

## Meta smoke checklist (roles-only)

1. Copy `.env.example` → `.env` and set real `META_VERIFY_TOKEN`, `META_APP_SECRET`, `META_PAGE_ACCESS_TOKEN`.
2. App Live/published; App Roles + role on IG Professional / Page; Connected Tools → Allow Access to Messages.
3. Permissions: `instagram_basic`, `instagram_manage_messages`, `pages_manage_metadata`.
4. Run API (`deka-api` or uvicorn); expose HTTPS (`ngrok`/`cloudflared`) → Callback `https://<host>/webhooks/meta` with the same verify token.
5. Subscribe fields `messages`; `POST /{PAGE_ID}/subscribed_apps` with Page token.
6. Tester with app role DMs the IG Pro account → expect stub reply `Deka ok: …`.

---

## Blockers

_Groq key required (`GROQ_API_KEY` or Groq key under `OPENROUTER_API_KEY`) for live notebook evals._
_Live Meta DM smoke needs tunnel + filled `META_*` secrets in local `.env`._
