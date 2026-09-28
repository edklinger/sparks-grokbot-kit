# Dashboard data contract

`dashboard/template.html` renders one JSON object, `SPARKS_DATA`. Build it, validate it with `scripts/validate_data.py`, then inject it with `scripts/build_dashboard.py`. `seed/dashboard-data.demo.json` is a complete, valid example: when in doubt, copy its shape.

All dates are ISO (`YYYY-MM-DD`, or full ISO datetimes where noted). All text is plain text; the page escapes it. Names that appear in `D.names` are automatically wrapped so present mode can shorten them to first names.

## Top level

| key | type | what it drives |
|---|---|---|
| `CONFIG` | object | `owner_name`, `owner_first`, `owner_aliases` (list), `company`, `slack_workspace` (subdomain, or empty), `locale` (optional BCP 47 tag such as `fr-FR`; defaults to the viewer's browser locale), `time_zone` (optional IANA name; defaults to the viewer's browser time zone), `page_title`, and optionally `news_areas` (`{area_key: label}`) and `notable_ids` (body ids that always get a permanent orrery label). |
| `DATA_THROUGH` | date | Header "Data through …". |
| `FEED_SNAP` | datetime | The "now" the calendar is briefed against. |
| `SOURCES` | list | Appendix corpus summary. Each is `{key, name, detail}`. Known keys with icons: gmail, whatsapp, slack, granola, calendar, linkedin, hubspot, notion, contacts, web. Any other key gets a generic icon. `detail` is one line: what was read, how deeply, and signals extracted. |
| `TB_NAMES` | object | Time budget: `{bucket_key: want name}` for each measurable want. |
| `TB_OTHER` | object | Time budget: `{bucket_key: label}` for non-want time (day job, admin, personal). |
| `PSENS_IDS` | list | Move ids removed entirely in present mode. |
| `PSENS_LIST` | list | Substrings; any card whose text contains one is removed in present mode. |
| `NEW_MOVES` | list | Move ids tagged NEW. |
| `PERSONAL_MOVES` | list | Move ids tagged PERSONAL. |
| `NEWS` | object | Network news (below). |
| `PROM` | list | Promise ledger (below). |
| `TIME` | object | Time budget (below). |
| `CORPUS` | list | Searchable corpus for the Ask box (below). |
| `D` | object | Preferences, actions and method (below). |
| `ORR` | object | The orbit (below). |
| `LDG` | object | The relationship ledger table (below). |
| `FEED` | list | The calendar briefing (below). |
| `MTITLES`, `PERSON2`, `EMAIL_NAME` | object | Optional overrides: `{}` is fine. `MTITLES` maps move id to a replacement title. `EMAIL_NAME` maps an email address to a display first name for present mode. |

## D

- `wants`: list of `{name, kind: stated|revealed|inferred, one_liner, quote|null, source, confidence?, depth?, evidence?: [[text, source], …]}`. Revealed wants need `evidence` and `confidence`.
- `moves`: list of suggested actions. Each move has these fields:
  - `id`: stable slug.
  - `title`: plain English.
  - `category`: one of Introduce, Reactivate, Repair, Rooms, Commercial, Angel, Platform, Ritual, Decide.
  - `people`: list of `{name, context, gmail, linkedin}`; the two links are search URLs or null.
  - `serves`: list of want names, which must match `wants[].name`.
  - `why`: text.
  - `evidence`: list of `{what, source, date, quote|null, where, link|null}`.
  - `action`: text.
  - `draft`: text or null. Multiple drafts are separated by `\n\n---\n`, and each starts with `[email to Name]` or `[whatsapp to Name]`.
  - `hold_note`: text or null.
  - `score`: `{fit, distance, timing, feasibility, total}`.
  - `headline`: `for-someone-else`, `for-owner`, `repair` or null. Exactly one move per value makes the headline trio.
  - `settled`: optional true, which hides the move from the default list.
- `chart`: `{move_id: {l: 0, r: 1, ls: "left-side need", rs: "right-side offer"}}` for two-person introductions.
- `chips`: list of `{id: move_id, species: convening|passion|timing|…, a, b}`, shown as featured collisions.
- `hunches`: list of `[title, text]`, for thin-evidence patterns.
- `names`: every person name that should be wrapped as a name (include the owner).
- `quotes`: short verbatim phrases to style as quotes where they appear in text.
- `stats`: list of `[label, value]`. Labels read by the page: People indexed, Person files, Preferences tracked, Haves, Passions, Unanswered asks, Promises extracted, Calendar events kept.
- `gaps`: list of text, for honest coverage gaps.
- `prov`: list of `[LABEL, meaning]` for RECORD, INFERENCE, MEASURED and WEB.

## ORR (the orbit)

- `clusters`: sector names. The last one should be `Wider network`, which renders as dust.
- `shell_names`: four ring names (Inner circle, Working orbit, Outer orbit, Deep field).
- `shell_gloss`: four one-line explanations of the rings.
- `indexed_total`: number (the page recomputes it).
- `bodies`: named people drawn as planets. Each is `{id, name, cluster, shell: 1-4, size: 1-5, months_since, dormant, active_move, moves: [move_id], meetings, label: always|hover|none, notable?: true}`. If any body is `notable` (or `CONFIG.notable_ids` is set), only those keep permanent labels; otherwise each body's own `label` is used. Aim for 30 to 200.
- `chords`: introduction lines between two bodies: `{a: body_id, b: body_id, score, fit, timing, title, move_id}`.
- `dn` (near dust, hoverable): parallel arrays `id, name, shell, size, ms (months since), mt (meetings)`, plus `always: [index]` and `mv: {index: [move_id]}`.
- `df` (far dust, points): parallel arrays `x, y, r, id, name`, plus `n3` (how many leading points belong to the outer orbit). The coordinates use a 1240 × 1240 plane centred at (620, 620). Outer orbit points sit at radius 380 to 440, and deep field points at 555 to 592.

## LDG (relationship ledger)

`cols` must be exactly: name, cluster, phone_known, meetings, ev_gmail, ev_granola, ev_slack, ev_whatsapp, ev_imessage, ev_linkedin, ev_other, weighted_mass, log_mass, multiplexity, reciprocity, vouched, owner_initiated, dormant, last_signal (YYYY-MM), months_since, tau, heat, bond, size, shell.

`rows` holds one array per person, in column order.

## PROM (promise ledger)

`{id, d: date, dir: owner_owes|owed_to_owner|mutual, w: 1-5, who, what, src, link|null, raw, closed?: date, fresh?: true}`

## NEWS

`{generated, items: [...], areas?: {area_key: label}, crm: [...], coverage: {people_scanned, people_total, not_searched: [], note}}`

Each item is `{who, org, kind, area?, headline, date, url, source, confidence: high|moderate|low, why_it_matters, fresh?}`.

- `kind` is one of: job_move, appointment, funding, exit, launch, partnership, press, award, leadership, shutdown, sector, other, crm_change.
- `area` is a free topic key; its display label comes from `NEWS.areas` (or `CONFIG.news_areas`), otherwise the key itself is shown.
- Public sources only. Every item carries its URL.

## FEED (calendar)

`{t: title, s: start datetime, e: end datetime, k: ext|int|ritual|personal, att: [names], who: context, help: what to do, sens?: 1, move?: move_id}`

## TIME (time budget)

`{window: "Q3 to date", src: "method sentence", agg: {bucket_key: {mins, n}}, ex: {bucket_key: [{t, h, n}]}}`

Bucket keys come from `TB_NAMES` and `TB_OTHER`.

## CORPUS (Ask box)

A list of `[person, date, kind, source, text]`, one row per extracted signal. Keep the text short and factual. This is what the Ask box searches.
