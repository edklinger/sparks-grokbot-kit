#!/usr/bin/env python3
"""Parse an mbox export (e.g. Google Takeout) into email JSONL (headers plus a short body snippet).
usage: python3 ingest_mbox.py mail.mbox out.jsonl [--owner you@example.com]"""
import mailbox, json, sys, email.utils, email.header
path, out = sys.argv[1], sys.argv[2]
owner = sys.argv[sys.argv.index("--owner")+1].lower() if "--owner" in sys.argv else ""
def dec(v):
    try: return str(email.header.make_header(email.header.decode_header(v or "")))
    except Exception: return v or ""
def body(m):
    part = m
    if m.is_multipart():
        part = next((p for p in m.walk() if p.get_content_type()=="text/plain"), None)
        if part is None: return ""
    try: return (part.get_payload(decode=True) or b"").decode(part.get_content_charset() or "utf-8","ignore")[:1500]
    except Exception: return ""
n, threads, dates = 0, set(), []
with open(out,"w",encoding="utf-8") as fo:
    for m in mailbox.mbox(path):
        try: d = email.utils.parsedate_to_datetime(m.get("Date")).date().isoformat()
        except Exception: d = ""
        frm = email.utils.parseaddr(m.get("From",""))
        rec = {"source":"mbox","date":d,"from_name":dec(frm[0]),"from":frm[1].lower(),
               "to":[a[1].lower() for a in email.utils.getaddresses(m.get_all("To",[])+m.get_all("Cc",[]))],
               "subject":dec(m.get("Subject","")),"thread":m.get("X-GM-THRID") or m.get("References","").split(" ")[0] or m.get("Message-ID",""),
               "outbound": bool(owner and frm[1].lower()==owner),"snippet":body(m)}
        fo.write(json.dumps(rec, ensure_ascii=False)+"\n"); n += 1; threads.add(rec["thread"])
        if d: dates.append(d)
print(f"{n} messages in {len(threads)} threads, {min(dates) if dates else '-'} to {max(dates) if dates else '-'}")
