#!/usr/bin/env python3
"""Same filename census on random samples from other NIH institutes: share of papers with a spreadsheet/CSV attachment."""
import json, random, re, sys, time, urllib.parse, collections, concurrent.futures as cf, threading
src=open('census.py').read(); exec(src.split("if __name__")[0])
TAB={"xlsx","xls","xlsm","csv","tsv","txt","tab","ods"}
INST={"NHLBI (heart, lung, blood)":"NHLBI NIH HHS","NIDDK (diabetes, digestive, kidney)":"NIDDK NIH HHS","NIMH (mental health)":"NIMH NIH HHS","NIA (aging)":"NIA NIH HHS","NINDS (neurological)":"NINDS NIH HHS"}
ACC2=ACC.replace("ACCESSION_TYPE:pdb)","ACCESSION_TYPE:pdb OR ACCESSION_TYPE:geo)")
out={}
for label,tag in INST.items():
    q=f'GRANT_AGENCY:"{tag}" AND PUB_YEAR:[2016 TO 2022] AND OPEN_ACCESS:y AND HAS_SUPPL:Y AND NOT {ACC2}'
    ids=[]; cursor="*"
    while len(ids)<3000:
        t,e=get(f"{EPMC}/search?query={urllib.parse.quote(q)}&format=json&pageSize=1000&resultType=lite&cursorMark={urllib.parse.quote(cursor)}")
        try: d=json.loads(t)
        except Exception: break
        res=d.get("resultList",{}).get("result",[]); ids+=[r["pmcid"] for r in res if r.get("pmcid")]; pop=d.get("hitCount")
        nxt=d.get("nextCursorMark")
        if not res or not nxt or nxt==cursor: break
        cursor=nxt; time.sleep(0.5)
    random.seed(2026); samp=random.sample(ids,min(300,len(ids))); recs=[]; lock=threading.Lock()
    def one(pmc):
        x,e=get(f"{EPMC}/{pmc}/fullTextXML"); files=parse(x) if x else []
        with lock: recs.append({"pmcid":pmc,"err":e,"files":files})
    with cf.ThreadPoolExecutor(8) as ex: list(ex.map(one,samp))
    ok=[r for r in recs if not r["err"]]; tab=[r for r in ok if any(f["ext"] in TAB for f in r["files"])]
    out[label]={"population":pop,"sampled":len(samp),"readable":len(ok),"papers_with_spreadsheet":len(tab),"share":round(len(tab)/max(len(ok),1)*100,1),"spreadsheet_files":sum(1 for r in ok for f in r["files"] if f["ext"] in TAB)}
    print(label, out[label], flush=True)
    json.dump(out,open("data/institutes.json","w"),indent=1)
print("done")
