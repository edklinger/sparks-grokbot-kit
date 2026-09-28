#!/usr/bin/env python3
"""Parse WhatsApp chat exports (.txt, 'Without media') into message JSONL.
usage: python3 ingest_whatsapp.py out.jsonl export1.txt [export2.txt ...]
Handles Android 'DD/MM/YYYY, HH:MM - Name: text' and iOS '[DD/MM/YYYY, HH:MM:SS] Name: text'.
Continuation lines belong to the previous message. System lines (no sender) are skipped."""
import re, sys, json, os
A = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+(\d{1,2}:\d{2})(?::\d{2})?\s*(?:[ap]\.?m\.?)?\s+-\s+([^:]+?):\s(.*)$", re.I)
I = re.compile(r"^\u200e?\[(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+(\d{1,2}:\d{2})(?::\d{2})?\s*(?:[ap]\.?m\.?)?\]\s+([^:]+?):\s(.*)$", re.I)
out, files = sys.argv[1], sys.argv[2:]
total = 0
with open(out, "a", encoding="utf-8") as fo:
    for f in files:
        chat = re.sub(r"^WhatsApp Chat (with|-)\s*", "", os.path.splitext(os.path.basename(f))[0])
        cur, n, senders, dates = None, 0, set(), []
        def flush():
            global total
            if cur:
                fo.write(json.dumps(cur, ensure_ascii=False) + "\n"); total += 1
        for line in open(f, encoding="utf-8", errors="ignore"):
            line = line.rstrip("\n")
            m = A.match(line) or I.match(line)
            if m:
                flush()
                d, mo, y, hm, who, text = m.groups()
                y = int(y); y = y + 2000 if y < 100 else y
                date = f"{y:04d}-{int(mo):02d}-{int(d):02d}"
                cur = {"source":"whatsapp","chat":chat,"date":date,"time":hm,"sender":who.strip(),"text":text}
                n += 1; senders.add(who.strip()); dates.append(date)
            elif cur is not None:
                cur["text"] += "\n" + line
        flush(); cur = None
        print(f"{os.path.basename(f)}: {n} messages, {len(senders)} senders, {min(dates) if dates else '-'} to {max(dates) if dates else '-'}")
print(f"total {total} messages -> {out}")
