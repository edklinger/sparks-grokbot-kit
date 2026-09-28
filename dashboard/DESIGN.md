# Sparks design system

The look is Sparks' own: a pencil-study orrery on warm paper, with one ember accent. It is not any company's brand. Every value below is already inside `dashboard/template.html`; this file exists so the look can be reproduced or extended without reading the CSS.

## Colour tokens

| token | value | use |
|---|---|---|
| `--paper` | `#FAF7F2` | page background |
| `--ink` | `#1E1B16` | body text, rules, primary buttons |
| `--ember` | `#C2410C` | the single accent: kickers, links, introduction lines, NEW tags, scores |
| `--amber` / `--amber-line` | `#92400E` / `#B45309` | time running out, dotted "closing window" lines |
| graphite | `#3A362F` | orrery bodies and labels |
| sepia | `#6B5B4A` | small-caps labels, PERSONAL tag outline |
| `--muted` / `--faint` | ink at 62% / 42% | secondary and tertiary text |
| `--hair` / `--hair2` | ink at 14% / 8% | hairlines and dividers |
| washes | ember or amber at 6 to 7% | hover and selected backgrounds |

Rule of thumb: ink and paper do 95% of the work. Ember appears only where the eye should land.

## Type

- **Serif** (`Georgia, 'Times New Roman', serif`): body copy, card text, italic intros. Base size 15px, line height 1.5.
- **Sans** (`system-ui, -apple-system, 'Segoe UI', sans-serif`): uppercase labels and headings with wide tracking (0.16em to 0.3em), 10 to 12px, weight 600 to 700.
- **Numerals** (`'Times New Roman'` stack): big hero stats, with tabular figures where numbers line up.
- There are no web fonts. Everything is a system stack, so the page renders identically offline and on mobile.

## Layout

- Max width 1180px, with 32px gutters. Sections are 64px apart.
- The chapters (Orbit, Calendar, News, Preferences, Actions, Promises, Appendix) are collapsible sections with a top navigation that shows counts.
- The hero is a two-column layout: "Discover your luck surface area" with four stats on the left, and the top five opportunities on the right.
- The orrery is SVG with a viewBox of -25 -25 1290 1290, centred at (620, 620).
  - Four rings sit at radii 150, 295, 440 and 575.
  - Named clusters get angular sectors proportional to the square root of their size, with 3 degree gutters.
  - The wider network is drawn as dust.
  - Introductions are ember chords between two bodies. A dotted chord means the timing window is closing.
  - Zoom and pan are scoped to the orrery, and deeper zoom reveals more names.

## Motion

The logo (`dashboard/logo.svg`, self-contained) has four layers: orbit arcs rotating once every 52 seconds, a breathing glow on a 6.5-second cycle, twinkling points on staggered 2.2 to 4.2-second cycles, and the SPARKS wordmark. Orrery bodies drift slowly along their rings, at a different rate per ring. Everything stops under `prefers-reduced-motion`.

## Components worth knowing

- **Action card.** Category, title, score out of 25, why, evidence with dated sources, next step, and a copyable draft. Actions can be marked done, later or not for me.
- **Tags.** `.tagnew` has an ember fill and white text. `.tagpersonal` has a dotted sepia outline and no fill, and is deliberately quiet.
- **Present mode.** The eye icon in the header shows first names only, hides quotes, and removes sensitive cards entirely. Nothing is merely masked.
- **Ask box** (press `/`). Free-text search over the corpus and the people index.
- **Refresh.** Opens a modal holding the rebuild prompt.
