#!/usr/bin/env python3
"""Build deposit-ready packages for the best rescued datasets (no upload is performed).
Each package = the original file + DataCite-style metadata.json + README.md. Only CC BY / CC0 papers, native spreadsheets, primary data."""
import csv, json, os, zipfile, io, re, collections
import openpyxl
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(HERE,"data"); OUT=os.path.join(HERE,"packages")
S=json.load(open(os.path.join(DATA,"sample.json"))); meta={p["pmcid"]:p for p in S["papers"]}
GEO=set(json.load(open(os.path.join(DATA,"sample_geo_flagged.json"))))
F=[f for f in csv.DictReader(open(os.path.join(DATA,"files.csv"))) if f["class"].startswith("dataset") and f["native"]=="True" and f["derived"]!="True" and meta[f["pmcid"]].get("license") in ("cc by","cc0") and f["pmcid"] not in GEO]
F.sort(key=lambda f:-int(f["max_rows"] or 0))
seen=set(); picks=[]
for f in F:
    if f["pmcid"] in seen: continue
    seen.add(f["pmcid"]); picks.append(f)
    if len(picks)>=8: break
os.makedirs(OUT,exist_ok=True)
for f in picks:
    p=meta[f["pmcid"]]; d=os.path.join(OUT,f["pmcid"]); os.makedirs(d,exist_ok=True)
    z=zipfile.ZipFile(os.path.join(DATA,"zips",f["pmcid"]+".zip")); name=next(x for x in z.namelist() if os.path.basename(x)==f["file"]); b=z.read(name)
    open(os.path.join(d,f["file"]),"wb").write(b)
    sheets=[]
    if f["ext"] in (".xlsx",".xlsm"):
        wb=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
        for ws in wb.worksheets:
            rows=[r for _,r in zip(range(3),ws.iter_rows(values_only=True))]
            hdr=[str(c)[:30] for r in rows for c in r if c is not None][:12]
            sheets.append({"sheet":ws.title,"first_cells":hdr})
    creators=[{"name":a.strip()} for a in (p.get("authorString") or "").rstrip(".").split(",") if a.strip()][:20]
    md={"identifier":{"identifier":"TO BE ASSIGNED ON DEPOSIT","identifierType":"DOI"},
        "titles":[{"title":f"Supplementary dataset ({f['file']}) from: {p['title'].rstrip('.')}"}],
        "creators":creators,"publisher":"Rescued from PubMed Central open-access article; original publisher: "+p["journalTitle"],
        "publicationYear":p["pubYear"],"resourceType":{"resourceTypeGeneral":"Dataset","resourceType":"Supplementary data table"},
        "relatedIdentifiers":[{"relatedIdentifier":p.get("doi"),"relatedIdentifierType":"DOI","relationType":"IsSupplementTo"},
                              {"relatedIdentifier":f["pmcid"],"relatedIdentifierType":"PMCID","relationType":"IsSourceOf"}],
        "rightsList":[{"rights":p["license"].upper(),"rightsURI":"https://creativecommons.org/licenses/by/4.0/" if p["license"]=="cc by" else "https://creativecommons.org/publicdomain/zero/1.0/"}],
        "fundingReferences":[{"funderName":"National Cancer Institute"}],
        "subjects":[{"subject":S["cancer"]}],
        "descriptions":[{"descriptionType":"Abstract","description":f"Tabular supplementary data file originally attached to the article. Largest table: {f['max_rows']} rows x {f['max_cols']} columns. Content type (heuristic): {f['kind']}. Sheets: "+"; ".join(s["sheet"] for s in sheets)}],
        "sizes":[f"{int(f['bytes'])//1024} KB"],"formats":[f["ext"].lstrip(".")],
        "provenance":{"source":"Europe PMC supplementaryFiles endpoint","harvested":"2026-09-22","original_filename":f["file"],"sheets":sheets}}
    json.dump(md,open(os.path.join(d,"metadata.json"),"w"),indent=1)
    open(os.path.join(d,"README.md"),"w").write(f"# {md['titles'][0]['title']}\n\nOriginal article: https://doi.org/{p.get('doi')} ({p['journalTitle']}, {p['pubYear']}), PMC: {f['pmcid']}\nLicense inherited from article: {p['license'].upper()}\n\nThis file was attached to the article as supplementary material and had no dataset-level record, DOI, or catalogue entry of its own. It is packaged here, unmodified, with DataCite-style metadata so it can be deposited in an NIH-recognized generalist repository and listed in the Index of NCI Studies.\n\nLargest table: {f['max_rows']} rows x {f['max_cols']} cols. Sheets: {', '.join(s['sheet'] for s in sheets) or '-'}\n")
    print(f"{f['pmcid']} {f['file']:40} rows={f['max_rows']:>6} {f['kind']:8} {p['journalTitle'][:22]:22} {p['title'][:60]}")
print(f"\n{len(picks)} packages -> packages/")
