# Brand

Visual system for Deka. Light mode only. Monochromatic: one brand hue, roles defined by contrast.

---

## Direction

- Clean, calm hospitality UI
- Single hue (`#3793ca`), no secondary palette
- Contrast drives hierarchy, not extra colors

---

## Color (light)

Seed: `#3793ca` · Background: `#ffffff`

| Role | Hex | Min contrast | Use |
|------|-----|--------------|-----|
| **Brand** | `#3793ca` | 4.5 vs bg when used as text/icon* | Accents, primary actions, key UI |
| **Text strong** | `#0e57af` | 4.5 | Primary copy, headings |
| **Text weak** | `#4576b0` | 4.5 | Secondary / non-priority copy |
| **Stroke strong** | `#8994a1` | 3.1 | Interactive outlines (inputs, secondary buttons) |
| **Stroke weak** | `#dde1e6` | — | Decorative dividers / soft borders |

\*Raw `#3793ca` on white is ~3.4. Prefer **Text strong** for body/links on white, or darken Brand until ≥4.5. On Brand fills, use dark text (not white).

### How roles are derived

1. **Brand** — client hue; pick the variant with best contrast vs background (≥4.5 when the token sits on the bg).
2. **Text strong** — lower lightness, raise saturation → dark brand for primary text (≥4.5).
3. **Text weak** — from Text strong: raise lightness, lower saturation → secondary text (≥4.5).
4. **Stroke strong** — lower lightness & saturation → mid gray-blue for interactive chrome (≥3.1).
5. **Stroke weak** — lighter, desaturated → decorative only (no contrast target).

---

## Spacing

Base `1rem` = `16px`. Prefer this scale; skip steps rather than invent values.

| Token | rem | Example |
|-------|-----|---------|
| `space-1` | `0.25rem` | Icon gap inside a button; tight chip padding |
| `space-2` | `0.5rem` | Label → input gap; inline icon + text |
| `space-3` | `0.75rem` | Compact button / input vertical padding |
| `space-4` | `1rem` | Default control padding; gap between form fields |
| `space-5` | `1.5rem` | Card / section inner padding |
| `space-6` | `2rem` | Stack between page blocks |
| `space-8` | `3rem` | Major section separation |
| `space-10` | `4rem` | Page edge / hero breathing room |

---

## Borders & radius

### Width

| Token | rem | Example |
|-------|-----|---------|
| `border` | `0.0625rem` | Default outlines, dividers, input borders |
| `border-thick` | `0.125rem` | Focus ring, selected state, primary emphasis |

Colors: interactive chrome → **Stroke strong**; dividers / soft frames → **Stroke weak**.

### Radius

| Token | rem | Example |
|-------|-----|---------|
| `radius-sm` | `0.25rem` | Checkboxes, small chips, tags |
| `radius-md` | `0.5rem` | Buttons, inputs, selects |
| `radius-lg` | `0.75rem` | Cards, panels, modals |
| `radius-xl` | `1rem` | Large sheets, feature panels |
| `radius-full` | `9999px` | Avatars, icon-only circular controls |

---

## Photography

_Style TBD (venue atmosphere: bars / cafés)._

---

## Voice

- Clear, calm, helpful
- Hospitality-oriented (bars and cafés)
- Avoid jargon unless operators need it
