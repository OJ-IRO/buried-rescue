#!/usr/bin/env python3
"""Same filename census on a random sample of NCI open-access papers published 2024-2025 (after the DMS policy took effect)."""
import json, random, time, urllib.parse, threading, concurrent.futures as cf
src=open('census.py').read(); exec(src.split("if __name__")[0])
TAB={"xlsx","xls","xlsm","csv","tsv","txt","tab","ods"}
ACC2=ACC.replace("ACCESSION_TYPE:pdb)","ACCESSION_TYPE:pdb OR ACCESSION_TYPE:geo)")
out={}
for label,yrs in (("2024-2025","[2024 TO 2025]"),):
    q=f'GRANT_AGENCY:"NCI NIH HHS" AND PUB_YEAR:{yrs} AND OPEN_ACCESS:y AND HAS_SUPPL:Y AND NOT {ACC2}'
    ids=[]; cursor="*"; pop=None
    while len(ids)<6000:
        t,e=get(f"{EPMC}/search?query={urllib.parse.quote(q)}&format=json&pageSize=1000&resultType=lite&cursorMark={urllib.parse.quote(cursor)}")
        try: d=json.loads(t)
        except Exception: time.sleep(5); continue
        res=d.get("resultList",{}).get("result",[]); ids+=[(r["pmcid"],r.get("pubYear"),r.get("journalTitle")) for r in res if r.get("pmcid")]; pop=d.get("hitCount")
        nxt=d.get("nextCursorMark")
        if not res or not nxt or nxt==cursor: break
        cursor=nxt; time.sleep(0.5)
    random.seed(2026); samp=random.sample(ids,min(600,len(ids))); recs=[]; lock=threading.Lock()
    def one(p):
        x,e=get(f"{EPMC}/{p[0]}/fullTextXML"); files=parse(x) if x else []
        with lock: recs.append({"pmcid":p[0],"year":p[1],"journal":p[2],"err":e,"files":files})
    with cf.ThreadPoolExecutor(8) as ex: list(ex.map(one,samp))
    ok=[r for r in recs if not r["err"]]; tab=[r for r in ok if any(f["ext"] in TAB for f in r["files"])]
    by={y:(sum(1 for r in tab if r["year"]==y), sum(1 for r in ok if r["year"]==y)) for y in sorted({r["year"] for r in ok})}
    out[label]={"population":pop,"sampled":len(samp),"readable":len(ok),"papers_with_spreadsheet":len(tab),"share":round(len(tab)/max(len(ok),1)*100,1),"by_year":by,"spreadsheet_files":sum(1 for r in ok for f in r["files"] if f["ext"] in TAB)}
    print(label,out[label],flush=True)
json.dump(out,open("data/post2023.json","w"),indent=1); print("done")
