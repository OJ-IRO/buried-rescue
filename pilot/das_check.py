#!/usr/bin/env python3
"""Validate the population filter: do 'no accession' papers really cite no data repository?
Sample N papers from the census population, fetch full text, extract the data-availability section
and any repository mentions anywhere in the text, and classify."""
import json, random, re, gzip, sys, time, urllib.request, collections, concurrent.futures as cf, threading
N=int(sys.argv[1]) if len(sys.argv)>1 else 500
ids=json.load(open("data/census_ids_v2.json")); random.seed(2026); samp=random.sample(ids,N)
UA={"User-Agent":"ods-rescue-das/1.0","Accept-Encoding":"gzip"}
REPO=re.compile(r"\b(GSE\d{4,7}|GSM\d{5,8}|SRP\d{5,8}|PRJNA\d{4,8}|PRJEB\d{4,8}|SRR\d{5,9}|ERP\d{5,8}|phs\d{6}|EGA[SD]\d{8,11}|E-MTAB-\d+|PXD\d{5,7}|MTBLS\d+|MSV\d{9}|syn\d{6,9}|zenodo\.org|figshare\.com|datadryad|dryad\.|osf\.io|github\.com|gitlab\.com|mendeley data|cbioportal|proteomexchange|dbGaP|dbgap|Gene Expression Omnibus|Sequence Read Archive|ArrayExpress|ImmPort|GDC|Genomic Data Commons|TCGA|cancer genome atlas|CCLE|DepMap|Synapse|MassIVE|PRIDE|MetaboLights|BioProject|BioStudies|Kaggle|Data Dryad|Harvard Dataverse|dataverse|Xena|GTEx|ENCODE|ClinicalTrials\.gov|NCT\d{8})\b", re.I)
DAS=re.compile(r"<sec[^>]*>\s*<title>[^<]*(?:data|code|material)s?\s+(?:and\s+\w+\s+)?availability[^<]*</title>.*?</sec>|<(?:sec|p|notes)[^>]*>\s*(?:<title>)?\s*(?:availability of data[^<]{0,80}|data (?:and (?:code|materials?) )?availability(?: statement)?)\s*(?:</title>)?.*?</(?:sec|p|notes)>", re.I|re.S)
def get(u):
    for k in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90) as r:
                b=r.read(); return (gzip.decompress(b) if r.headers.get("Content-Encoding")=="gzip" else b).decode("utf-8","replace")
        except Exception: time.sleep(3)
    return None
def strip(x): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",x or "")).strip()
out=[]; lock=threading.Lock()
def one(p):
    x=get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{p['pmcid']}/fullTextXML")
    if not x: rec={"pmcid":p["pmcid"],"err":1}
    else:
        m=DAS.search(x); das=strip(m.group(0))[:600] if m else ""
        body=strip(re.sub(r"(?is)<ref-list>.*?</ref-list>","",x))  # ignore reference list
        hits=sorted(set(h.group(0).lower() for h in REPO.finditer(body)))
        dash=sorted(set(h.group(0).lower() for h in REPO.finditer(das))) if das else []
        acc=[h for h in hits if re.match(r"(gse|gsm|srp|prjna|prjeb|srr|erp|phs|ega|e-mtab|pxd|mtbls|msv|syn|nct)\d",h)]
        rec={"pmcid":p["pmcid"],"year":p["pubYear"],"journal":p["journalTitle"],"has_das":bool(das),"das":das[:300],"das_hits":dash,"any_hits":hits[:15],"accessions":acc[:10]}
    with lock: out.append(rec)
with cf.ThreadPoolExecutor(6) as ex: list(ex.map(one,samp))
json.dump(out,open("data/das_check.json","w"),indent=0)
ok=[r for r in out if not r.get("err")]
print(f"sampled {N}, readable {len(ok)}")
print(f"has a data-availability section: {sum(r['has_das'] for r in ok)} ({sum(r['has_das'] for r in ok)/len(ok):.0%})")
print(f"DAS mentions a repository/accession: {sum(bool(r['das_hits']) for r in ok)} ({sum(bool(r['das_hits']) for r in ok)/len(ok):.0%})")
print(f"ANY accession-like ID in body text (GSE/SRP/PRJNA/phs/PXD/...): {sum(bool(r['accessions']) for r in ok)} ({sum(bool(r['accessions']) for r in ok)/len(ok):.0%})")
print(f"mentions a public resource anywhere (incl. TCGA/CCLE/GEO reuse): {sum(bool(r['any_hits']) for r in ok)} ({sum(bool(r['any_hits']) for r in ok)/len(ok):.0%})")
c=collections.Counter(h for r in ok for h in r['any_hits']); print("top mentions:", c.most_common(15))
das_txt=collections.Counter()
for r in ok:
    d=r['das'].lower()
    if not d: das_txt['no DAS']+=1
    elif re.search(r"supplement|supporting information|within the (article|paper|manuscript)|in the (article|paper|manuscript)|included in this",d): das_txt['DAS: in paper/supplement']+=1
    elif re.search(r"upon (reasonable )?request|on request|from the corresponding author",d): das_txt['DAS: on request']+=1
    elif r['das_hits']: das_txt['DAS: names repository']+=1
    else: das_txt['DAS: other']+=1
print("DAS categories:", dict(das_txt))
