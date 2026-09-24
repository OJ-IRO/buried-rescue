#!/usr/bin/env python3
"""Fetch grant lists for the corrected census population; map NCI activity codes to mechanism families."""
import json, urllib.request, urllib.parse, time, gzip, collections, re
ids=[p["pmcid"] for p in json.load(open("data/census_ids_v2.json"))]
UA={"User-Agent":"ods-rescue/1.0","Accept-Encoding":"gzip"}; out={}
try: out=json.load(open("data/grants.json"))
except Exception: pass
todo=[i for i in ids if i not in out]; print(len(out),"have",len(todo),"to fetch",flush=True)
for k in range(0,len(todo),40):
    q=" OR ".join(f"PMCID:{x}" for x in todo[k:k+40])
    u="https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="+urllib.parse.quote(q)+"&format=json&pageSize=100&resultType=core"
    for t in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=120) as r:
                b=r.read(); b=gzip.decompress(b) if r.headers.get("Content-Encoding")=="gzip" else b
            for x in json.loads(b)["resultList"]["result"]:
                gs=x.get("grantsList",{}).get("grant",[]) if isinstance(x.get("grantsList"),dict) else []
                out[x["pmcid"]]=[{"agency":g.get("agency"),"id":g.get("grantId")} for g in gs]
            for x in todo[k:k+40]: out.setdefault(x,[])
            break
        except Exception: time.sleep(5+5*t)
    if (k//40)%50==0: json.dump(out,open("data/grants.json","w")); print(k,flush=True)
    time.sleep(0.4)
json.dump(out,open("data/grants.json","w"))
fam=collections.Counter(); papers_by=collections.defaultdict(set)
for pmc,gs in out.items():
    for g in gs:
        if (g.get("agency") or "")!="NCI NIH HHS": continue
        m=re.match(r"\s*([A-Z]\d{2}|ZIA|Z01|ZIC)\s*[A-Z]{2}",(g.get("id") or "").upper())
        if m: code=m.group(1); papers_by[code].add(pmc)
print({k:len(v) for k,v in sorted(papers_by.items(), key=lambda x:-len(x[1]))[:20]})
