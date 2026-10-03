# Sparks for Grok Bot

Sparks turns everything in someone's inboxes, chats, calendar and meeting notes into a ranked, evidenced list of introductions, reconnections, repairs and decisions, then draws it as an orbital map of their network. Nothing is ever sent without approval.

This kit contains no personal data. The demo is built on a fictional network ("Alex Morgan", founder of "Harbourline"). Every name, company and number in `seed/` and `dashboard/demo.html` is invented.

## What is in the box

```
SUPER_PROMPT.md          the bot's instructions (paste into the main bot)
system/                  blank file-system-of-record templates (README contract, RULES, optional EXCLUDE, ledgers, state)
schema/                  event schema, person-file template, DATA_CONTRACT.md for the dashboard
scripts/                 ingest parsers (WhatsApp, LinkedIn archive, mbox, calendar), coverage report,
                         dashboard validator and builder, PII scanner, demo-data generator
dashboard/template.html  the dashboard, design fixed, data injected at build time
dashboard/demo.html      the dashboard rendered with the fictional seed: open it to see the target
dashboard/logo.svg       the animated Sparks mark, self-contained
dashboard/DESIGN.md      colours, type, layout and motion
seed/                    the fictional dataset behind the demo
```

## Install on Grok Bot (about 10 minutes)

1. **Create the bot.** Name: `Sparks`. Title: `Chief of staff for your network`. Description: `Reads your email, calendar, meeting notes, WhatsApp and LinkedIn; finds the introductions, reconnections and promises that matter; drafts the next step; never sends anything without approval.`
2. **Paste** `SUPER_PROMPT.md` (everything below its divider line) into the bot's instructions.
3. **Let the bot install the kit.** Nothing to upload. On its first run the bot downloads the latest release zip itself from `https://github.com/edklinger/sparks-grokbot-kit/releases/latest/download/sparks-grokbot-kit.zip` and unzips it into `~/sparks/`. The bot works from `~/sparks/system/` as its system of record and runs the scripts from `~/sparks/scripts/` in its terminal (Python 3, standard library only). **Fallback:** if the download fails (for example no network access), download `sparks-grokbot-kit.zip` from the [latest release](https://github.com/edklinger/sparks-grokbot-kit/releases/latest), drop it into the chat, and ask the bot to unzip it into `~/sparks/`.
4. **Connect plugins:** Gmail and Google Calendar at minimum, then Slack and a meeting-notes tool if you use them. Plugins are shared across bots on the account.
5. **Say "Set me up".** The bot walks you through each source one at a time (why it needs it and exactly how to grant access), interviews you briefly, then reads everything you have connected, with no exclusion questions. The first ingest can take hours (WhatsApp and LinkedIn often run overnight), with progress updates. It then shows the coverage report, builds your dashboard and gives you a short tour of it.
6. **Schedule it (optional).** The bot offers a weekly "Refresh sparks" routine (for example Monday at 06:30) and a daily calendar brief. Both stay off unless you say yes. You can also say "Refresh sparks" any time.

Check it worked: ask the bot to run `python3 ~/sparks/scripts/build_dashboard.py ~/sparks/dashboard/template.html ~/sparks/seed/dashboard-data.demo.json ~/sparks/demo.html`, then open the result. It should match `dashboard/demo.html`.

## Recommended: a three-bot team

xAI recommends narrow bots. Sparks splits cleanly into three, all sharing `~/sparks/`:

| bot | title | job | sections of SUPER_PROMPT |
|---|---|---|---|
| **Sparks Intake** | Keeps the corpus fresh | Onboarding, source discovery, ingestion, identity resolution, coverage report. Runs on a routine. | Platform, 0 to 3, 8 |
| **Sparks** | Chief of staff for your network | Extraction, scoring, the dashboard, answering questions about the network. | Platform, 0, 4, 5, 7, 8 |
| **Sparks Drafts** | Writes the next step | Drafts introductions and replies in the owner's voice, on the right thread and channel. Every send needs approval. | Platform, 0, 6, 8 |

Give each bot the full `SUPER_PROMPT.md`, plus one line at the top naming its sections. A single bot also works; the team is just more reliable on long runs.

## Things to know

- **Browser sources.** WhatsApp Web needs the owner to scan the QR code from their phone, and only shows what the phone has synced. LinkedIn in the browser risks account restrictions, so the prompt defaults to the LinkedIn data archive. The owner always signs in themselves; the bot never handles passwords.
- **Bots are not security boundaries** on Grok Bot. Every bot on the account can use the shared connections, so keep Sparks on a personal account.
- **Files beat memory.** The file contract in `system/README.md` is the source of truth. Bot memory is a convenience, not a record.
- **Before sharing anything outside,** run `python3 scripts/pii_scan.py <path> --names <list of real names>`.

## Customising the dashboard

Do not edit the HTML. Produce data that matches `schema/DATA_CONTRACT.md`, check it with `scripts/validate_data.py`, and build with `scripts/build_dashboard.py`. `CONFIG` sets the owner's name, company, locale and page title; everything else on the page is filled from the data.

## Sharing as a Grok Bot template

Once Sparks is running, open the bot's settings and use **Share as Template**, choosing Team or a public link. Templates carry the bot's instructions, skills, non-personal memories and first-party plugins. They do not carry scripts or code, so the bot downloads `sparks-grokbot-kit.zip` from the latest GitHub release on its first run. Only if that download fails does it ask the owner to drop the zip into the chat. Before you publish, check the template details: no personal memories should be in it.

---

*Sparks is an AI-native project by Ed Leon Klinger.*
