# Spec

Business requirements, goals, and scope for Deka.

---

## Product

Deka helps bars and cafés take and manage customer reservations through an AI agent. The agent runs the conversation from first contact through a confirmed booking.

---

## Goals

We want an agent that can take over day-to-day reservation work: handle bookings, answer menu questions, and make the process easier for the venue.

- Reduce manual reservation handling for venue staff
- Give customers a natural conversation path to book
- Keep reservation data reliable and easy to operate from the dashboard

---

## Vocabulary

- **Client** — diner / guest of the café
- **Process** — one reservation conversation unit (a client can have many processes)
- **Status** — `interested` | `reserved` | `confirmed`

---

## What we want to see

- How many processes the agent is handling, party size per booking, and which table or space is involved
- Per-process status: Interested / Reserved / Confirmed
- Client identity linked to each process

---

## In scope

For each process, capture and surface:

- Linked client (name / contact)
- Date and time received
- Current status
- Party size
- Space type (terrace, birthday areas, tables)
- Whether human intervention is required


---

## Out of scope

- Organizing or assigning scheduled tables on the floor plan
- Full conversational history with the agent
- Direct purchases and payments

---

## Success criteria

- More reservations without more time spent handling each one
