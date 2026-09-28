#!/usr/bin/env python3
"""Parse a LinkedIn data archive (the zip, or the unzipped folder).
usage: python3 ingest_linkedin.py <archive.zip|folder> <outdir>
Writes outdir/linkedin-messages.jsonl and outdir/linkedin-connections.jsonl, and prints counts."""
import csv, io, json, os, sys, zipfile
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
def open_member(name):
    if zipfile.is_zipfile(src):
        z = zipfile.ZipFile(src)
        for n in z.namelist():
            if n.lower().endswith(name.lower()): return io.TextIOWrapper(z.open(n), encoding="utf-8", errors="ignore")
    else:
        for dp,_,fs in os.walk(src):
            for f in fs:
                if f.lower() == name.lower(): return open(os.path.join(dp,f), encoding="utf-8", errors="ignore")
    return None
def rows(fh):
    lines = fh.read().splitlines()
    # Connections.csv starts with a 'Notes:' preamble; find the real header
    start = next((i for i,l in enumerate(lines) if l.startswith(("First Name","CONVERSATION ID","From","FROM"))), 0)
    return list(csv.DictReader(lines[start:]))
fh = open_member("messages.csv"); nm = 0; convs = set()
if fh:
    with open(os.path.join(outdir,"linkedin-messages.jsonl"),"w",encoding="utf-8") as fo:
        for r in rows(fh):
            g = lambda *k: next((r[x] for x in k if x in r and r[x]), "")
            rec = {"source":"linkedin","conversation":g("CONVERSATION ID"),"title":g("CONVERSATION TITLE"),
                   "date":g("DATE")[:10],"sender":g("FROM"),"to":g("TO"),"sender_url":g("SENDER PROFILE URL"),
                   "text":g("CONTENT")}
            fo.write(json.dumps(rec, ensure_ascii=False)+"\n"); nm += 1; convs.add(rec["conversation"])
fh = open_member("Connections.csv"); nc = 0
if fh:
    with open(os.path.join(outdir,"linkedin-connections.jsonl"),"w",encoding="utf-8") as fo:
        for r in rows(fh):
            rec = {"source":"linkedin","name":(r.get("First Name","")+" "+r.get("Last Name","")).strip(),
                   "url":r.get("URL",""),"email":r.get("Email Address",""),"company":r.get("Company",""),
                   "position":r.get("Position",""),"connected_on":r.get("Connected On","")}
            fo.write(json.dumps(rec, ensure_ascii=False)+"\n"); nc += 1
print(f"messages: {nm} in {len(convs)} conversations · connections: {nc}")
