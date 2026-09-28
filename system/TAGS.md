# Provenance tags

| field | meaning |
|---|---|
| `fresh` / `_new` | Arrived in the most recent intake. Clear it at the start of the next refresh, before new events are appended. |
| `_personal` | Came from a personal (lower-trust) feed, such as a personal mailbox. Permanent: it records provenance, not recency. |

The dashboard reads `fresh` on promises and news items, and the `NEW_MOVES` and `PERSONAL_MOVES` id lists for actions. It renders NEW first, then PERSONAL.

The personal tag is deliberately quiet. An unanswered personal email is weak evidence of a dropped ball when the relationship lives on chat.
