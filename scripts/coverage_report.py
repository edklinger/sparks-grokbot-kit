#!/usr/bin/env python3
"""Summarise everything ingested so far: per source, records, threads/chats, people, date range and signals.
usage: python3 coverage_report.py <raw_dir> [--sources-json out.json]
Reads every *.jsonl under raw_dir. Prints a markdown table; optionally writes the dashboard SOURCES list."""
import json, os, sys, collections
root = sys.argv[1]
S = collections.defaultdict(lambda: {"records":0,"threads":set(),"people":set(),"dates":[],"kinds":collections.Counter(),"transcripts":0})
for dp,_,fs in os.walk(root):
    for f in fs:
        if not f.endswith(".jsonl"): continue
        for line in open(os.path.join(dp,f), encoding="utf-8", errors="ignore"):
            try: r = json.loads(line)
            except Exception: continue
            s = S[r.get("source") or f.split(".")[0]]
            s["records"] += 1
            t = r.get("thread") or r.get("chat") or r.get("conversation")
            if t: s["threads"].add(t)
            for k in ("person","sender","from","from_name"):
                if r.get(k): s["people"].add(r[k])
            for a in r.get("attendees",[]) or []: s["people"].add(a)
            if r.get("date"): s["dates"].append(r["date"][:10])
            if r.get("kind"): s["kinds"][r["kind"]] += 1
            if r.get("transcript"): s["transcripts"] += 1
print("| source | records | threads/chats | people | from | to | signals by kind |\n|---|---|---|---|---|---|---|")
tot = collections.Counter(); srcs = []
for k,s in sorted(S.items(), key=lambda kv: -kv[1]["records"]):
    d = sorted(s["dates"]); kinds = ", ".join(f"{a} {b}" for a,b in s["kinds"].most_common(5)) or "-"
    print(f"| {k} | {s['records']:,} | {len(s['threads']):,} | {len(s['people']):,} | {d[0] if d else '-'} | {d[-1] if d else '-'} | {kinds} |")
    tot["records"] += s["records"]; tot["threads"] += len(s["threads"]); tot["transcripts"] += s["transcripts"]
    tot["signals"] += sum(s["kinds"].values())
    detail = f"{s['records']:,} records across {len(s['threads']):,} threads, {d[0] if d else '?'} to {d[-1] if d else '?'}"
    if s["kinds"]: detail += f"; {sum(s['kinds'].values()):,} signals extracted"
    srcs.append({"key":k.split("-")[0],"name":k.replace("-"," ").title(),"detail":detail})
allp = set().union(*[s["people"] for s in S.values()]) if S else set()
print(f"\n**Totals:** {len(S)} sources · {tot['records']:,} records · {tot['threads']:,} threads/chats · {tot['transcripts']:,} transcripts · {len(allp):,} distinct people/handles · {tot['signals']:,} signals")
if "--sources-json" in sys.argv:
    json.dump(srcs, open(sys.argv[sys.argv.index("--sources-json")+1],"w"), indent=1)
