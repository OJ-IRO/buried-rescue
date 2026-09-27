#!/usr/bin/env python3
"""For every NCI core project number behind a census paper with a spreadsheet attachment, fetch FY2016-2022 parent-award
dollars from NIH RePORTER. Writes data/reporter_dollars.json {core_num: {"total": $, "org": name, "fy": {...}}}."""
import json, re, collections, urllib.request, time, os
TAB={"xlsx","xls","xlsm","csv","tsv","txt","tab","ods"}
G=json.load(open("data/grants.json"))
R={}
for l in open("data/census_files.jsonl"):
    if l.strip(): r=json.loads(l); R[r["pmcid"]]=r
for l in open("data/census_rescan.jsonl"):
    if l.strip():
        r=json.loads(l)
        if not r.get("err"): R[r["pmcid"]]=r
sp={p for p,r in R.items() if not r.get("err") and any(f["ext"] in TAB for f in r["files"])}
core=collections.Counter()
for pmc,gs in G.items():
    if pmc not in sp: continue
    for g in gs:
        if (g.get("agency") or "")!="NCI NIH HHS": continue
        m=re.match(r"\s*([A-Z]\d{2}|UM\d|UG\d)\s*(CA\d{6})",(g.get("id") or "").upper())
        if m: core[m.group(1)+m.group(2)]+=1
out={}
if os.path.exists("data/reporter_dollars.json"): out=json.load(open("data/reporter_dollars.json"))
todo=[c for c in core if c not in out]; print(f"grants behind spreadsheet papers: {len(core)} | to fetch: {len(todo)}",flush=True)
def fetch(nums):
    res=[]; off=0
    while True:
        body=json.dumps({"criteria":{"project_nums":nums,"fiscal_years":list(range(2016,2023))},"include_fields":["ProjectNum","CoreProjectNum","FiscalYear","AwardAmount","SubprojectId","Organization","ActivityCode"],"limit":500,"offset":off}).encode()
        req=urllib.request.Request("https://api.reporter.nih.gov/v2/projects/search",data=body,headers={"Content-Type":"application/json","Accept":"application/json"})
        for t in range(4):
            try: d=json.load(urllib.request.urlopen(req,timeout=90)); break
            except Exception: time.sleep(3+3*t); d={}
        r=d.get("results",[]); res+=r
        if len(r)<500 or off>=14500: break
        off+=500
    return res
for k in range(0,len(todo),25):
    batch=todo[k:k+25]
    for r in fetch(batch):
        cp=r.get("core_project_num");
        if not cp or r.get("subproject_id"): continue
        o=out.setdefault(cp,{"total":0.0,"org":None,"fy":{}}); fy=str(r.get("fiscal_year")); amt=float(r.get("award_amount") or 0)
        o["total"]+=amt; o["fy"][fy]=o["fy"].get(fy,0)+amt
        org=(r.get("organization") or {}).get("org_name") if isinstance(r.get("organization"),dict) else None
        if org: o["org"]=org
    for c in batch: out.setdefault(c,{"total":0.0,"org":None,"fy":{}})
    if (k//25)%10==0: json.dump(out,open("data/reporter_dollars.json","w")); print(k,"...",flush=True)
    time.sleep(0.3)
json.dump(out,open("data/reporter_dollars.json","w"))
tot=sum(v["total"] for v in out.values()); print(f"done: {len(out)} grants, FY2016-2022 parent awards total ${tot/1e9:,.2f}B")
