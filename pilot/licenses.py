import json, urllib.request, urllib.parse, time, collections, gzip
ids=[p["pmcid"] for p in json.load(open("data/census_ids.json"))]
out="data/census_licenses.json"; lic={}
try: lic=json.load(open(out))
except Exception: pass
todo=[i for i in ids if i not in lic]; print(len(lic),"have,",len(todo),"to fetch",flush=True)
UA={"User-Agent":"ods-rescue-census/1.0","Accept-Encoding":"gzip"}
for k in range(0,len(todo),40):
    q=" OR ".join(f"PMCID:{x}" for x in todo[k:k+40])
    u="https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="+urllib.parse.quote(q)+"&format=json&pageSize=100&resultType=core"
    for t in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=120) as r:
                b=r.read(); b=gzip.decompress(b) if r.headers.get("Content-Encoding")=="gzip" else b
            d=json.loads(b); res=d["resultList"]["result"]
            for x in res: lic[x.get("pmcid")]=x.get("license") or ""
            for x in todo[k:k+40]: lic.setdefault(x,"")
            break
        except Exception: time.sleep(5+5*t)
    if (k//40)%50==0: json.dump(lic,open(out,"w")); print(k,flush=True)
    time.sleep(0.5)
json.dump(lic,open(out,"w")); print(collections.Counter(v or "untagged" for v in lic.values()).most_common())
