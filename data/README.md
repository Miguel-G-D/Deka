# Data

Business reference content for the agent (menus, hours, policies, venue facts).

Not application runtime database files—those live under `backend/` infrastructure.

## Venue (8onzas)

| File | Purpose |
|------|---------|
| `venue/8onzas-profile.json` | Name, greeting, hours, spaces, reservation rules |
| `venue/8onzas-menu.json` | Categories, items, prices |
| `tests/menu_cases.json` | Unified A1 eval cases (product id / hours / unknown) |

Lab notebook: `lab/01_menu_agent_v1.ipynb` (LangChain `create_agent` + OpenRouter).
