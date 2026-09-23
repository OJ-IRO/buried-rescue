#!/usr/bin/env python3
"""Merge the v2-parser rescan into the census, restrict to the corrected population, and write census_summary_v3.json."""
import json, collections
TAB={"xlsx","xls","xlsm","csv","tsv","txt","tab","ods"}; XL={"xlsx","xls","xlsm"}
v2={p["pmcid"] for p in json.load(open("data/census_ids_v2.json"))}; lic=json.load(open("data/census_licenses.json"))
R={}
for l in open("data/census_files.jsonl"):
    if l.strip(): r=json.loads(l); R[r["pmcid"]]=r
before=sum(len(r["files"]) for r in R.values() if r["pmcid"] in v2 and not r.get("err"))
for l in open("data/census_rescan.jsonl"):
    if l.strip():
        r=json.loads(l)
        if not r.get("err"): R[r["pmcid"]]=r   # v2 parser supersedes
allr=[r for r in R.values() if r["pmcid"] in v2]; ok=[r for r in allr if not r.get("err")]
tabp=[r for r in ok if any(f["ext"] in TAB for f in r["files"])]; tabf=[f for r in ok for f in r["files"] if f["ext"] in TAB]; xlf=[f for f in tabf if f["ext"] in XL]
L=collections.Counter((lic.get(r["pmcid"]) or "untagged") for r in tabp); free=sum(v for k,v in L.items() if k in ("cc by","cc0"))
freef=sum(1 for r in tabp if lic.get(r["pmcid"]) in ("cc by","cc0") for f in r["files"] if f["ext"] in TAB)
sz=[f["size"] for f in xlf if f.get("size")]
S={"population":len(v2),"readable":len(ok),"unreadable":len(allr)-len(ok),"attachments":sum(len(r["files"]) for r in ok),"attachments_before_parser_fix":before,
   "papers_with_tabular":len(tabp),"share_tabular":round(len(tabp)/len(ok)*100,1),"tabular_files":len(tabf),"excel_files":len(xlf),"excel_gb":round(sum(sz)/1e9,1),
   "free_papers":free,"free_share":round(free/len(tabp)*100,1),"free_files":freef,"licenses":dict(L.most_common()),
   "by_year":{y:[sum(1 for r in tabp if r["year"]==y), sum(1 for r in ok if r["year"]==y)] for y in sorted({r["year"] for r in ok})},
   "top_journals":collections.Counter(r["journal"] for r in tabp).most_common(10)}
json.dump(S,open("data/census_summary_v3.json","w"),indent=1)
print(f"FINAL CENSUS (corrected population, v2 parser): population {S['population']:,} | readable {S['readable']:,} | attachments {S['attachments']:,} (was {before:,} before parser fix)")
print(f"papers with spreadsheet/CSV: {S['papers_with_tabular']:,} ({S['share_tabular']}%) | files {S['tabular_files']:,} (Excel {S['excel_files']:,}, {S['excel_gb']} GB) | CC BY/CC0 {free:,} papers ({S['free_share']}%), {freef:,} files")
print("by year:", {y:f"{a/b:.0%}" for y,(a,b) in S["by_year"].items()}); print("top journals:", S["top_journals"][:6])
