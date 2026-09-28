#!/usr/bin/env python3
"""Validate a SPARKS_DATA JSON file against schema/DATA_CONTRACT.md.
usage: python3 validate_data.py data.json      (exit code 1 on any error)"""
import json, sys
LDG_COLS = ["name","cluster","phone_known","meetings","ev_gmail","ev_granola","ev_slack","ev_whatsapp","ev_imessage",
            "ev_linkedin","ev_other","weighted_mass","log_mass","multiplexity","reciprocity","vouched","owner_initiated",
            "dormant","last_signal","months_since","tau","heat","bond","size","shell"]
CATS = {"Introduce","Reactivate","Repair","Rooms","Commercial","Angel","Platform","Ritual","Decide"}
errs, warns = [], []
def E(m): errs.append(m)
def W(m): warns.append(m)
d = json.load(open(sys.argv[1], encoding="utf-8"))
for k,t in {"CONFIG":dict,"DATA_THROUGH":str,"SOURCES":list,"NEWS":dict,"PROM":list,"TIME":dict,"CORPUS":list,
            "D":dict,"ORR":dict,"LDG":dict,"FEED":list,"TB_NAMES":dict,"TB_OTHER":dict}.items():
    if k not in d: E(f"missing top-level key {k}")
    elif not isinstance(d[k], t): E(f"{k} should be {t.__name__}")
if errs: print("\n".join("ERROR "+e for e in errs)); sys.exit(1)
c = d["CONFIG"]
for k in ["owner_name","owner_first","company"]:
    if not c.get(k): E(f"CONFIG.{k} is empty")
D = d["D"]
for k in ["wants","moves","chart","chips","hunches","names","quotes","stats","gaps","prov"]:
    if k not in D: E(f"D.{k} missing")
wn = {w.get("name") for w in D.get("wants",[])}
ids = set()
heads = {}
for m in D.get("moves",[]):
    mid = m.get("id","?")
    if mid in ids: E(f"duplicate move id {mid}")
    ids.add(mid)
    for k in ["id","title","category","people","serves","why","evidence","action"]:
        if k not in m: E(f"move {mid}: missing {k}")
    if m.get("category") not in CATS: E(f"move {mid}: category {m.get('category')!r} not in {sorted(CATS)}")
    for s in m.get("serves",[]):
        if s not in wn: E(f"move {mid}: serves {s!r}, which is not a want name")
    sc = m.get("score")
    if sc is None or "total" not in sc: E(f"move {mid}: score.total missing")
    h = m.get("headline")
    if h: heads.setdefault(h, []).append(mid)
    for p in m.get("people",[]):
        if "name" not in p: E(f"move {mid}: a person has no name")
for h in ["for-someone-else","for-owner","repair"]:
    n = len(heads.get(h,[]))
    if n != 1: W(f"headline {h!r} has {n} moves (want exactly 1)")
for cid in D.get("chart",{}):
    if cid not in ids: E(f"D.chart refers to unknown move {cid}")
for ch in D.get("chips",[]):
    if ch.get("id") not in ids: E(f"D.chips refers to unknown move {ch.get('id')}")
O = d["ORR"]
bids = {b.get("id") for b in O.get("bodies",[])}
for b in O.get("bodies",[]):
    if b.get("shell") not in (1,2,3,4): E(f"body {b.get('id')}: shell must be 1-4")
    if b.get("cluster") not in O.get("clusters",[]): E(f"body {b.get('id')}: cluster {b.get('cluster')!r} not in ORR.clusters")
    for mv in b.get("moves",[]):
        if mv not in ids: W(f"body {b.get('id')}: unknown move {mv}")
for ch in O.get("chords",[]):
    if ch.get("a") not in bids or ch.get("b") not in bids: E(f"chord {ch.get('move_id')}: endpoint is not a body")
for part, keys in [("dn",["id","name","shell","size","ms","mt"]),("df",["x","y","r","id","name"])]:
    arr = O.get(part,{})
    lens = {k: len(arr.get(k,[])) for k in keys}
    if len(set(lens.values())) > 1: E(f"ORR.{part} arrays differ in length: {lens}")
if len(O.get("shell_names",[])) != 4: E("ORR.shell_names needs 4 entries")
L = d["LDG"]
if L.get("cols") != LDG_COLS: E("LDG.cols must match the contract exactly (see DATA_CONTRACT.md)")
for i,r in enumerate(L.get("rows",[])):
    if len(r) != len(LDG_COLS): E(f"LDG row {i} has {len(r)} values, expected {len(LDG_COLS)}"); break
for p in d["PROM"]:
    if p.get("dir") not in ("owner_owes","owed_to_owner","mutual"): E(f"promise {p.get('id')}: bad dir {p.get('dir')!r}")
for i,r in enumerate(d["CORPUS"][:5000]):
    if not (isinstance(r,list) and len(r)==5): E(f"CORPUS row {i} must be [person,date,kind,source,text]"); break
for f in d["FEED"]:
    for k in ["t","s","e","k"]:
        if k not in f: E(f"FEED item {f.get('t')!r}: missing {k}")
for k in d["TIME"].get("agg",{}):
    if k not in d["TB_NAMES"] and k not in d["TB_OTHER"]: W(f"TIME bucket {k!r} is in neither TB_NAMES nor TB_OTHER")
for w in warns: print("WARN ", w)
for e in errs: print("ERROR", e)
print(f"{len(errs)} errors, {len(warns)} warnings · {len(D.get('moves',[]))} moves, {len(O.get('bodies',[]))} bodies, {len(L.get('rows',[]))} ledger rows")
sys.exit(1 if errs else 0)
