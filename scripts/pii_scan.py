#!/usr/bin/env python3
"""Scan files for personal data before sharing anything outside.
usage: python3 pii_scan.py <path> [--names names.txt] [--allow allow.txt]
Flags email addresses, phone numbers, postcodes and any name listed in names.txt (one per line).
allow.txt lists strings that are fine to keep (e.g. fictional demo names). Exit code 1 if anything is found."""
import re, sys, os
args = sys.argv[1:]
root = args[0]
def load(flag):
    if flag in args:
        return [l.strip() for l in open(args[args.index(flag)+1], encoding="utf-8") if l.strip()]
    return []
names, allow = load("--names"), set(load("--allow"))
PAT = {
 "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
 "phone": re.compile(r"(?<![\w.])(?:\+44\s?7\d{3}|07\d{3})\s?\d{3}\s?\d{3}(?!\d)|\+\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}"),
 "uk_postcode": re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}\b"),
}
SAFE_EMAIL = re.compile(r"@(example\.(com|org|net)|test)$", re.I)
hits = 0
files = [root] if os.path.isfile(root) else [os.path.join(dp,f) for dp,_,fs in os.walk(root) for f in fs]
for p in files:
    try: t = open(p, encoding="utf-8", errors="ignore").read()
    except Exception: continue
    for kind, rx in PAT.items():
        for m in set(rx.findall(t)):
            s = m if isinstance(m,str) else m[0]
            if s in allow or (kind=="email" and SAFE_EMAIL.search(s)): continue
            print(f"{kind:12s} {p}: {s}"); hits += 1
    for n in names:
        if n in t and n not in allow:
            print(f"{'name':12s} {p}: {n}"); hits += 1
print(f"\n{hits} potential personal-data hits in {len(files)} files")
sys.exit(1 if hits else 0)
