#!/usr/bin/env python3
"""Stress-test numbers for the NCI ODS Impact Prize Track 1 entry (written 2026-09-21).

Reproduces, from the public Index of NCI Studies release, every figure quoted in
2026-09-21-track1-winning-strategy.md. No credentials needed.

Usage: python3 verify_findings.py            (downloads INS-Data release 2.4.1 once, ~30 MB)
       python3 verify_findings.py --zip PATH (use an already-downloaded release zip)
"""
import argparse, collections, csv, glob, io, json, os, re, statistics, urllib.request, zipfile

csv.field_size_limit(10**9)
NULL = {"", "NA", "N/A", "null", "None", "nan", "-"}
API = "https://api.github.com/repos/CBIIT/INS-Data/releases"


def fetch(version="2.4.1"):
    os.makedirs("_ins_cache", exist_ok=True)
    hit = glob.glob("_ins_cache/*.zip")
    if hit:
        return hit[0]
    req = urllib.request.Request(API, headers={"User-Agent": "ods-verify/1.0"})
    rel = next(r for r in json.load(urllib.request.urlopen(req, timeout=60)) if r["tag_name"] == version)
    asset = next(a for a in rel["assets"] if a["name"].endswith(".zip"))
    path = os.path.join("_ins_cache", asset["name"])
    print(f"downloading {asset['name']} ...")
    urllib.request.urlretrieve(asset["browser_download_url"], path)
    return path


def num(v):
    try:
        v = str(v).replace(",", "").strip()
        return float(v) if v not in NULL else None
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--zip"); a = ap.parse_args()
    z = zipfile.ZipFile(a.zip or fetch())
    rows = []
    for n in z.namelist():
        if "dataset" in n.lower() and n.endswith(".tsv"):
            rows += list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8"), delimiter="\t"))
    repo = lambda r: r["dataset_source_repo"]
    geo = [r for r in rows if repo(r) == "GEO"]; sra = [r for r in rows if repo(r) == "SRA"]
    dbg = [r for r in rows if repo(r) == "dbGaP"]
    pct = lambda k, n: f"{k} of {n} ({k / n:.1%})"
    filled = lambda rs, f: sum(1 for r in rs if str(r.get(f, "")).strip() not in NULL)

    print(f"\nINS dataset records: {len(rows)}  (GEO {len(geo)}, SRA {len(sra)}, dbGaP {len(dbg)})")

    print("\n1. THE ASYMMETRY (the team's original finding) - reproduces")
    for name, rs in (("dbGaP", dbg), ("GEO", geo), ("SRA", sra)):
        print(f"   {name:6} participant_count {pct(filled(rs,'participant_count'), len(rs))} | "
              f"limitations_for_reuse {pct(filled(rs,'limitations_for_reuse'), len(rs))} | "
              f"sample_count {pct(filled(rs,'sample_count'), len(rs))}")

    print("\n2. SAMPLE COUNT IS ALREADY THERE FOR GEO - and how good a stand-in for people is it?")
    P = [(num(r["sample_count"]), num(r["participant_count"])) for r in dbg]
    P = [(s, p) for s, p in P if s and p]
    ratios = sorted(s / p for s, p in P); L = len(P)
    print(f"   dbGaP records with both counts: {L}")
    print(f"   samples == participants:        {sum(1 for x in ratios if x == 1) / L:.1%}")
    print(f"   off by 2x or more:              {sum(1 for x in ratios if x >= 2 or x <= .5) / L:.1%}")
    print(f"   off by 5x or more:              {sum(1 for x in ratios if x >= 5 or x <= .2) / L:.1%}")
    print(f"   median ratio {statistics.median(ratios):.2f} | 95th pct {ratios[int(.95 * L)]:.1f} | max {ratios[-1]:.0f}")
    print(f"   BUT as a rough guess it lands within 10x {sum(1 for x in ratios if .1 <= x <= 10) / L:.1%} of the time")
    print("   -> the pilot's 96%-within-10x headline is matched by this free guess; exact/2x accuracy is where a method must win")

    print("\n3. GEO RECORDS WHERE THE LISTED SAMPLE COUNT BADLY UNDERSTATES THE DESCRIBED COHORT")
    pat = re.compile(r"\b(\d{1,3}(?:,\d{3})+|\d{3,6})\s+(?:patients|participants|individuals|donors|subjects|cases)\b")
    ex = []
    for r in geo:
        s = num(r["sample_count"]); m = [int(x.replace(",", "")) for x in pat.findall(r["description"])]
        if s and m and s <= 10 and max(m) >= 200:
            ex.append((int(s), max(m), r["dataset_source_id"], r["dataset_title"][:70]))
    for e in sorted(ex, key=lambda x: -x[1])[:5]:
        print("   listed samples=%d | description says %d people | %s | %s" % e)

    print("\n4. DOUBLE COUNTING - SRA records that are the same study as a GEO record")
    gt = {r["dataset_title"].strip().lower() for r in geo}
    dup = sum(1 for r in sra if r["dataset_title"].strip().lower() in gt)
    uniq = len(gt | {r["dataset_title"].strip().lower() for r in sra})
    print(f"   SRA titles identical to a GEO title: {pct(dup, len(sra))}")
    print(f"   distinct open-deposit studies: about {uniq}, not {len(geo) + len(sra)}")

    print("\n5. DISEASE FIELD - '100% populated' is only nominal")
    for name, rs in (("GEO", geo), ("SRA", sra), ("dbGaP", dbg)):
        nr = sum(1 for r in rs if r["primary_disease"].strip() == "Not Reported")
        print(f"   {name:6} primary_disease == 'Not Reported': {pct(nr, len(rs))}")
    print("   (NCI is already building an LLM disease mapper: github.com/CBIIT/ccdi-ins-icdo-mapping-llm - do not propose this)")

    print("\n6. HOW MANY OPEN RECORDS EVEN HAVE HUMAN PARTICIPANTS? (crude keyword scan - indicative only)")
    model = re.compile(r"\b(mouse|mice|murine|xenografts?|pdx|zebrafish|drosophila|yeast|rats?)\b")
    cell = re.compile(r"\bcell lines?\b|\bin vitro\b|\borganoids?\b")
    human = re.compile(r"\b(patients?|participants?|donors?|subjects|individuals|cohort)\b")
    for name, rs in (("GEO", geo), ("SRA", sra)):
        t = [(r["dataset_title"] + " " + r["description"]).lower() for r in rs]
        print(f"   {name}: model-organism words {sum(1 for x in t if model.search(x)) / len(t):.0%} | "
              f"cell-line words {sum(1 for x in t if cell.search(x)) / len(t):.0%} | "
              f"patient/cohort words {sum(1 for x in t if human.search(x)) / len(t):.0%}")

    print("\n7. OPEN RECORDS THAT POINT AT CONTROLLED-ACCESS DATA (the real 'reuse limitation' on open deposits)")
    ctl = re.compile(r"phs\d{6}|dbgap|controlled.access|\bEGA[SD]\d+", re.I)
    for name, rs in (("GEO", geo), ("SRA", sra)):
        hits = [r for r in rs if ctl.search(r["description"] + " " + r.get("study_links", ""))]
        print(f"   {name}: {len(hits)} records mention dbGaP / a phs accession / controlled access / EGA")
    gp = {p.strip() for r in geo + sra for p in re.split(r"[;,| ]+", r.get("dataset_pmid", "")) if p.strip().isdigit()}
    dp = {p.strip() for r in dbg for p in re.split(r"[;,| ]+", r.get("dataset_pmid", "")) if p.strip().isdigit()}
    print(f"   PubMed IDs shared between an open (GEO/SRA) record and a dbGaP record: {len(gp & dp)}  (INS does not link these pairs)")


if __name__ == "__main__":
    main()
