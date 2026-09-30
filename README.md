# Buried Rescue

Evidence and working files for a Track 1 (Ideas) entry to the **NCI Office of Data Sharing Impact Prize** (deadline 2026-10-05).

**The finding.** Before 2023, cancer scientists shared data by attaching spreadsheets to papers. Across the 26,228 NCI-funded open-access papers from 2016–2022 that have supplementary files and no text-mined data-repository accession, **4,759 (18.9%) carry a spreadsheet attachment, 15,458 files in all**, listed in no dataset catalogue. Opening the files in four random samples of 300 papers (glioblastoma, breast, colorectal, leukemia; papers with a GEO accession excluded) confirms **18.8% of papers hold a genuine data table (14.5% as a native spreadsheet)**, and 83% of those papers are CC BY or CC0. The same census on five other NIH institutes gives 15–24%. An independent methods review on 2026-09-23 found and fixed a filter bug; the corrections are documented in `pilot/PILOT_REPORT.md`.

**The proposal.** Find, sort, describe, deposit (or register) and catalogue those datasets in the Index of NCI Studies, then keep the links alive.

Live site: https://attachment-rescue.vercel.app

## Layout

| Path | What |
|---|---|
| `draft/essay-v5.md`, `draft/Narrative.pdf` | The narrative (four prompts + AI disclosure, ≤2,500 words) |
| `draft/supporting-evidence.html`, `draft/Supporting_Evidence.pdf` | One-page evidence sheet |
| `demo/` | Reuse demonstration: three rescued glioma tables joined, pooled survival, cross-table analysis |
| `pilot/PILOT_REPORT.md` | Method, results, hand check, census, four-cancer replication, corrections after review, NIH-wide census |
| `pilot/rescue_pilot.py` | `sample` / `fetch` / `classify` / `report` for one cancer type (`PILOT_DATA=data_<cancer>`) |
| `pilot/census.py`, `pilot/licenses.py`, `pilot/institutes.py`, `pilot/das_check.py` | Full-population attachment census via Europe PMC full text; licenses; other-institute samples; filter validation |
| `pilot/peek.py` | Print the first rows of any attachment, for hand-checking |
| `pilot/package.py` → `pilot/packages/` | Eight deposit-ready datasets with DataCite-style metadata (nothing uploaded yet) |
| `pilot/data*/` | Per-cancer samples, file-level and paper-level classifications; `data/census_files.jsonl` is the raw census |
| `site/` | The public page (static; served by Vercel) |
| `2026-09-21-track1-winning-strategy.md` | Earlier strategy notes on a different thesis, kept for the record |

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install openpyxl xlrd python-docx pandas pdfplumber
cd pilot
../.venv/bin/python census.py ids && ../.venv/bin/python census.py scan && ../.venv/bin/python census.py report
PILOT_DATA=data_breast_cancer ../.venv/bin/python rescue_pilot.py sample --cancer "breast cancer" --n 300 --seed 20260923
PILOT_DATA=data_breast_cancer ../.venv/bin/python rescue_pilot.py fetch && ... classify && ... report
```

All sources are public (Europe PMC). No credentials are needed. Downloaded attachments (`pilot/data*/zips/`) are excluded from the repo and regenerate on `fetch`.

## Prior work this builds on

Gobeill et al. 2025 (extraction of 36 M PMC supplementary files); PLOS and Springer Nature/BMC Figshare mirroring of new supplements; Federer 2018, Colavizza 2020, Federer 2022 on data availability and link durability. Citations in the essay and pilot report.

Generative AI (Anthropic Claude) assisted with code and text. Every number is reproducible from the scripts here.
