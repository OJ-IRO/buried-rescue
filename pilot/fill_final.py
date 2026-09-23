#!/usr/bin/env python3
"""Fill {{PLACEHOLDERS}} in essay, report, evidence sheet and site from census_summary_v3.json; print the values used."""
import json, re, os
S=json.load(open("pilot/data/census_summary_v3.json"))
files=S["tabular_files"]; papers=S["papers_with_tabular"]
# ranges: paper rate 81% dataset among spreadsheet papers; file rate 70%; discount 15% (filter) and 13.5% (figshare) -> low; no discount -> high
lo_p=round(papers*0.81*0.85*0.865/100)*100; hi_p=round(papers*0.81/100)*100
lo_f=round(files*0.70*0.85*0.865/500)*500; hi_f=round(files*0.70/500)*500
V={"{{FILES}}":f"{files:,}","{{ATTACH}}":f"{S['attachments']:,}","{{EXCEL}}":f"{S['excel_files']:,}","{{EXCEL_GB}}":f"{S['excel_gb']}","{{FREE_FILES}}":f"{S['free_files']:,}",
   "{{RANGE_PAPERS}}":f"{lo_p:,} to {hi_p:,}","{{RANGE_FILES}}":f"{lo_f:,} to {hi_f:,}"}
for f in ("draft/essay-v4.md","pilot/PILOT_REPORT.md","draft/supporting-evidence.html","site/index.html"):
    t=open(f).read()
    for k,v in V.items(): t=t.replace(k,v)
    left=re.findall(r"{{[A-Z_]+}}",t); open(f,"w").write(t); print(f, "remaining placeholders:", left)
print(json.dumps(V,indent=1))
