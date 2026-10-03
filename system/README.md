# Sparks: the file contract

This is the contract. A fresh session with zero context should be able to read this and resume.

## Layout

```
system/
  README.md            this file
  RULES.md             the owner's standing preferences
  EXCLUDE.md           optional; empty by default (nothing is excluded)
  TAGS.md              the fresh and personal provenance tags
  _state.json          per-source watermarks and blockers
  _index.json          identity index (derived; rebuilt each run)
  me/profile.md        the owner: role, wants, interview notes
  people/<slug>.md     person files (summary sections derived; log is separate)
  people/<slug>.log.md per-person interaction log (APPEND-ONLY)
  wants/wants.yaml     every want, have and passion with decay state (derived)
  ledgers/             commitments, introductions, reciprocity, decisions (APPEND-ONLY)
  raw/<YYYY-MM>/       cached source extractions per run (APPEND-ONLY)
  sparks/<YYYY-MM>.md  the ranked spark list per run (derived)
```

## Rules

Append-only, never regenerated: `people/*.log.md`, `ledgers/`, `raw/`.
Derived, safe to rebuild from scratch: person-file summaries, `_index.json`, `wants/wants.yaml`, `sparks/`, the dashboard data and HTML.

- Never hand-edit a derived file. Fix the input or the generator instead.
- Never regenerate a log. Appending is the only legal write.
- Decisions in `ledgers/decisions.log` survive regeneration. A dismissed spark never comes back.

## Deterministic IDs

Kind prefix plus `sha1(person|normalised text)[:8]`. Prefixes: `W-` want, `H-` have, `P-` passion, `PR-` promise, `A-` unanswered ask, `I-` intro, `V-` vouched, `D-` decision, `F-` fact.

## Absorbing a data drop

- **LinkedIn archive zip:** `Connections.csv` becomes index rows. `messages.csv` is the complete message history and a first-class conversation source. `Invitations.csv` provides unanswered-ask signals.
- **mbox:** parse with Python's `mailbox`.
- **WhatsApp `.txt` export:** header lines look like `DD/MM/YYYY, HH:MM - Name: message`; continuation lines belong to the previous message.
- **Calendar:** normalise with `scripts/ingest_calendar.py`.

Every drop follows the same steps:

1. Parse.
2. Normalise to `schema/event.schema.json`.
3. Write to `raw/<run>/`.
4. Dedupe.
5. Resolve identities.
6. Append to logs.
7. Regenerate derived files.

## Tiering

- **Person file:** anyone with real two-way interaction or involvement in a spark.
- **Index row:** everyone else.
- Promotion is automatic on new interaction. Never demote.

## Each run ships

1. The dashboard.
2. `sparks/<run>.md`.
3. One batched set of merge questions.
4. Honest gaps: what was blocked, missing or thin.
