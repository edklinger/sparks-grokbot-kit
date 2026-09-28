#!/usr/bin/env python3
"""Inject a SPARKS_DATA JSON file into the dashboard template.
usage: python3 build_dashboard.py template.html data.json out.html"""
import json, sys
tpl, data, out = sys.argv[1:4]
t = open(tpl, encoding="utf-8").read()
d = json.load(open(data, encoding="utf-8"))
blob = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
assert "/*__SPARKS_DATA__*/null" in t, "placeholder missing"
open(out, "w", encoding="utf-8").write(t.replace("/*__SPARKS_DATA__*/null", blob, 1))
print(f"wrote {out} ({len(blob)//1024} KB of data)")
