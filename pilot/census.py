#!/usr/bin/env python3
"""Census of supplementary attachments across ALL NCI-funded open-access papers (2016-2022) that have
supplementary files and cite no data repository. Reads each paper's full-text XML from Europe PMC and
records every attachment's filename and extension. No files are downloaded.

  census.py ids      -> data/census_ids.json
  census.py scan     -> data/census_files.jsonl  (resumable; --workers N)
  census.py report
"""
import argparse, collections, gzip, io, json, os, re, sys, threading, time, urllib.request, urllib.parse, concurrent.futures as cf
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(HERE,"data"); EPMC="https://www.ebi.ac.uk/europepmc/webservices/rest"
UA={"User-Agent":"ods-rescue-census/1.0 (research)","Accept-Encoding":"gzip"}
ACC="(ACCESSION_TYPE:gen OR ACCESSION_TYPE:sra OR ACCESSION_TYPE:dbgap OR ACCESSION_TYPE:ega OR ACCESSION_TYPE:arrayexpress OR ACCESSION_TYPE:pride OR ACCESSION_TYPE:bioproject OR ACCESSION_TYPE:metabolights OR ACCESSION_TYPE:pdb)"
Q=f'GRANT_AGENCY:"NCI NIH HHS" AND PUB_YEAR:[2016 TO 2022] AND OPEN_ACCESS:y AND HAS_SUPPL:Y AND NOT {ACC}'
TAB={"xlsx","xls","xlsm","csv","tsv","txt","tab","ods"}

def get(url, timeout=120, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=timeout) as r:
                b=r.read()
                if r.headers.get("Content-Encoding")=="gzip": b=gzip.decompress(b)
                return b.decode("utf-8","replace"), None
        except Exception as e:
            err=str(e)[:60]
            if "404" in err: return None, "404"
            time.sleep(2+3*k)
    return None, err

def cmd_ids(a):
    ids=[]; cursor="*"
    while True:
        for k in range(6):
            t,e=get(f"{EPMC}/search?query={urllib.parse.quote(Q)}&format=json&pageSize=1000&resultType=lite&cursorMark={urllib.parse.quote(cursor)}")
            try: d=json.loads(t); assert "resultList" in d; break
            except Exception: d={}; time.sleep(5)
        res=d.get("resultList",{}).get("result",[])
        for r in res:
            if r.get("pmcid"): ids.append({k:r.get(k) for k in ("pmcid","pubYear","journalTitle","license","doi")})
        nxt=d.get("nextCursorMark"); print(f"{len(ids)} / {d.get('hitCount')}",flush=True)
        if not res or not nxt or nxt==cursor: break
        cursor=nxt
    json.dump(ids,open(os.path.join(DATA,"census_ids.json"),"w")); print("saved",len(ids))

HREF=re.compile(r'<supplementary-material\b[^>]*>(.*?)</supplementary-material>',re.S)
MEDIA=re.compile(r'<(?:media|graphic|inline-supplementary-material)\b[^>]*?xlink:href="([^"]+)"[^>]*?(?:mimetype="([^"]*)")?',re.S)
MIME=re.compile(r'mimetype="([^"]*)"(?:\s+mime-subtype="([^"]*)")?')
def parse(xml):
    files=[]
    for block in HREF.findall(xml):
        for m in re.finditer(r'<(?:media|graphic|inline-supplementary-material)\b([^>]*)>',block):
            attrs=m.group(1); h=re.search(r'xlink:href="([^"]+)"',attrs)
            if not h: continue
            fn=h.group(1); ext=os.path.splitext(fn.lower())[1].lstrip(".")
            mm=MIME.search(attrs); mime=(mm.group(1)+"/"+(mm.group(2) or "")).strip("/") if mm else ""
            tail=block[m.end():m.end()+1500]
            sz=re.search(r'<\?size (\d+)\?>',tail); cap=re.search(r'<caption>(.*?)</caption>',tail,re.S)
            files.append({"f":fn,"ext":ext,"mime":mime,"size":int(sz.group(1)) if sz else None,
                          "cap":re.sub(r'<[^>]+>','',cap.group(1)).strip()[:120] if cap else ""})
    # de-dup by filename
    seen=set(); out=[]
    for f in files:
        if f["f"] in seen: continue
        seen.add(f["f"]); out.append(f)
    return out

def cmd_scan(a):
    ids=json.load(open(os.path.join(DATA,"census_ids.json"))); outp=os.path.join(DATA,"census_files.jsonl")
    done=set()
    if os.path.exists(outp):
        for line in open(outp): done.add(json.loads(line)["pmcid"])
    todo=[p for p in ids if p["pmcid"] not in done]; print(f"{len(done)} done, {len(todo)} to scan",flush=True)
    lock=threading.Lock(); n=[0]; fh=open(outp,"a")
    def one(p):
        t,e=get(f"{EPMC}/{p['pmcid']}/fullTextXML")
        rec={"pmcid":p["pmcid"],"year":p["pubYear"],"journal":p["journalTitle"],"license":p.get("license"),"err":e,"files":parse(t) if t else []}
        with lock:
            fh.write(json.dumps(rec)+"\n"); n[0]+=1
            if n[0]%50==0: fh.flush(); print(f"{n[0]}/{len(todo)}",flush=True)
    with cf.ThreadPoolExecutor(a.workers) as ex: list(ex.map(one,todo))
    fh.close(); print("scan complete",flush=True)

def cmd_report(a):
    R=[json.loads(l) for l in open(os.path.join(DATA,"census_files.jsonl"))]
    n=len(R); ok=[r for r in R if not r["err"]]; withfiles=[r for r in ok if r["files"]]
    print(f"papers scanned {n} | full text readable {len(ok)} | with >=1 attachment listed in XML {len(withfiles)}")
    allf=[f for r in ok for f in r["files"]]; ext=collections.Counter(f["ext"] or f["mime"] or "?" for f in allf)
    print(f"\nattachments listed: {len(allf)}"); [print(f"  {k:12}{v:7}") for k,v in ext.most_common(18)]
    tabp=[r for r in ok if any(f["ext"] in TAB for f in r["files"])]; tabf=[f for f in allf if f["ext"] in TAB]
    xl=[f for f in allf if f["ext"] in ("xlsx","xls","xlsm")]
    print(f"\nPAPERS with >=1 spreadsheet/CSV/TSV attachment: {len(tabp)} of {len(ok)} ({len(tabp)/len(ok):.1%})")
    print(f"SPREADSHEET/CSV/TSV FILES total: {len(tabf)}  (Excel alone: {len(xl)})")
    lic=collections.Counter((r["license"] or "untagged") for r in tabp); print("licenses of those papers:",dict(lic.most_common()))
    print(f"  freely re-depositable (cc by / cc0): {sum(v for k,v in lic.items() if k in ('cc by','cc0'))}")
    yr=collections.Counter(r["year"] for r in tabp); print("by year:",dict(sorted(yr.items())))
    print("top journals:",collections.Counter(r["journal"] for r in tabp).most_common(10))

if __name__=="__main__":
    ap=argparse.ArgumentParser(); s=ap.add_subparsers(dest="c",required=True)
    s.add_parser("ids").set_defaults(fn=cmd_ids); x=s.add_parser("scan"); x.add_argument("--workers",type=int,default=8); x.set_defaults(fn=cmd_scan); s.add_parser("report").set_defaults(fn=cmd_report)
    a=ap.parse_args(); a.fn(a)
