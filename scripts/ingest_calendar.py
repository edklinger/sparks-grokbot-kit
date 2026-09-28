#!/usr/bin/env python3
"""Normalise calendar exports into event JSONL and a people-by-meetings summary.
usage: python3 ingest_calendar.py out.jsonl --owner you@example.com file1 [file2 ...]
Accepts Google Calendar API JSON (list_events results, {"events":[...]} or {"items":[...]}) and .ics files.
Drops cancelled events, events the owner declined, and solo blocks (OOO, focus, travel, lunch)."""
import json, re, sys, collections
args = sys.argv[1:]
out = args[0]; owner = args[args.index("--owner")+1].lower(); files = args[args.index("--owner")+2:]
SOLO = re.compile(r"^(ooo|out of office|holiday|travel|lunch|block|focus|deep work|wfh|hold)\b", re.I)
evs = []
def add(title, date, atts, declined=False, recurring=False):
    others = sorted({a.lower() for a in atts if a and a.lower()!=owner})
    if declined or (not others and SOLO.search(title or "")): return
    evs.append({"source":"calendar","date":date,"title":(title or "(no title)").strip(),"attendees":others,"recurring":recurring})
for f in files:
    if f.lower().endswith(".ics"):
        cur = None
        for line in open(f, encoding="utf-8", errors="ignore"):
            line = line.strip()
            if line == "BEGIN:VEVENT": cur = {"att":[]}
            elif line == "END:VEVENT" and cur:
                if cur.get("status") != "CANCELLED": add(cur.get("t"), cur.get("d",""), cur["att"], recurring="rr" in cur)
                cur = None
            elif cur is not None:
                if line.startswith("SUMMARY"): cur["t"] = line.split(":",1)[1]
                elif line.startswith("DTSTART"): v = line.split(":",1)[1]; cur["d"] = f"{v[:4]}-{v[4:6]}-{v[6:8]}"
                elif line.startswith("ATTENDEE"): m = re.search(r"mailto:([^\s;]+)", line, re.I); m and cur["att"].append(m.group(1))
                elif line.startswith("STATUS"): cur["status"] = line.split(":",1)[1]
                elif line.startswith("RRULE"): cur["rr"] = 1
    else:
        data = json.load(open(f, encoding="utf-8"))
        for e in data.get("events") or data.get("items") or []:
            if e.get("status") == "cancelled": continue
            s = e.get("start",{}); d = (s.get("dateTime") or s.get("date") or "")[:10]
            atts = [a.get("email","") for a in e.get("attendees",[]) if not a.get("resource")]
            dec = any(a.get("self") and a.get("responseStatus")=="declined" for a in e.get("attendees",[]))
            add(e.get("summary"), d, atts, dec, bool(e.get("recurringEventId") or e.get("recurrence")))
with open(out,"w",encoding="utf-8") as fo:
    for e in sorted(evs, key=lambda x: x["date"]): fo.write(json.dumps(e, ensure_ascii=False)+"\n")
c = collections.Counter(a for e in evs for a in e["attendees"])
print(f"{len(evs)} events kept · {len(c)} people · top: " + ", ".join(f"{a} ({n})" for a,n in c.most_common(10)))
