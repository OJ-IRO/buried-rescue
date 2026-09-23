# Supplementary-data rescue pilot: results (2026-09-22)

**Question.** Of NCI-funded, open-access papers on one cancer type (2016-2022) that have supplementary files but cite no
data repository, how many carry a real, reusable dataset?

**Answer.** About one in five. In glioblastoma, 61 of 300 randomly sampled papers (20.3%) hold at least one genuine data
table in their attachments. 46 of those (15.3%) are native spreadsheets under a license that permits re-deposit today.

Everything here is reproducible: `rescue_pilot.py sample|fetch|classify|report`, `peek.py`, `package.py`, and the raw
outputs in `data/`. No credentials were used. Nothing was uploaded anywhere.

## Method
- Population: Europe PMC query for `GRANT_AGENCY:"NCI NIH HHS"`, 2016-2022, open access, has supplementary files, no
  text-mined accession for GEO/SRA/dbGaP/EGA/ArrayExpress/PRIDE/BioProject/MetaboLights/PDB, title or abstract mentions
  glioblastoma. Population = 630 papers. Random sample of 300 (seed 20260922).
- Retrieved supplementary files for 289 (9 returned no files, 2 exceeded the 120 MB cap). 656 files total.
- Every spreadsheet, CSV, Word and PDF file was opened. A file counts as a **dataset** if its largest table has >= 50 rows
  and >= 3 columns, or >= 1,000 rows. PDF and Word tables count only if they are numeric grids, and peer-review letters,
  reporting summaries and reprints are excluded.
- Hand check: 45 files opened and judged by a person (30 called dataset, 15 called not-dataset).

## Results

| Per paper (n=300) | Count | Share |
|---|---|---|
| At least one dataset file | 61 | 20.3% |
| ...as a native spreadsheet / CSV | 46 | 15.3% |
| ...only as a table inside a PDF or Word file | 15 | 5.0% |
| Small tables only (10-49 rows) | 26 | 8.7% |
| No tabular data (figures, methods, videos) | 194 | 64.7% |
| No supplements retrievable | 11 | 3.7% |

| Per file (n=656) | Count | Share |
|---|---|---|
| Documents (PDF/Word, no numeric grid) | 343 | 52% |
| Dataset, medium (50-999 rows) | 75 | 11% |
| Dataset, large (>= 1,000 rows) | 46 | 7% |
| Small table | 59 | 9% |
| Media, images, other | 108 | 16% |

- 121 dataset files. Largest-table size: median 427 rows, 90th percentile 8,259, maximum 118,273.
- Formats: 95 xlsx, 8 xls, 9 docx, 8 pdf, 1 txt.
- Content (heuristic): 43 omics tables (gene or probe rows), 49 numeric measurement tables, 22 mixed, 7 clinical/cohort.
- Licenses of the 61 dataset papers: 46 CC BY, 5 CC BY-NC, 7 CC BY-NC-ND, 3 untagged. CC BY allows re-deposit unchanged.
- Journals: Nature Communications 14, Scientific Reports 5, Neuro-Oncology Advances 4, Oncotarget 4, PLOS ONE 3.

## Hand check (45 files)
- 30 files called "dataset": **30 of 30 are genuine data tables.** By content, 17 are primary data (expression matrices,
  patient cohort tables with age/sex/stage/survival, peak lists, per-sample counts, ChIP peaks) and 13 are derived results
  (differential expression lists, GO/KEGG enrichment, GSEA). The automatic "derived" flag undercounts this; the honest
  split is roughly half primary, half derived.
- 15 files called "not dataset": 14 correct (figure PDFs, methods, a peer-review letter, a reporting summary). 1 missed a
  17-row genetic association table inside a PDF.
- Earlier, before the PDF rules were tightened, review letters and reprints were being counted as data. That is fixed and
  is the reason PDF-derived datasets are reported separately.

## What it means
- Glioblastoma alone: about 20% of 630 = roughly 128 papers with rescuable datasets, ~95 freely re-depositable.
- Across all NCI-funded open-access papers with supplements and no accession (~32,000): a naive extrapolation gives
  roughly 6,500 papers and, at ~2 dataset files per paper, on the order of 13,000 dataset files. Treat this as an
  order-of-magnitude estimate from one cancer type; other fields may differ.
- About half of rescued tables are derived results rather than raw measurements. Both have reuse value (meta-analysis,
  benchmarking, teaching), but the proposal should say this plainly.

## Deposit-ready packages
`packages/` holds 8 examples, each with the unmodified file, DataCite-style `metadata.json` (title, creators, license,
related article DOI, PMC ID, funder, sizes, sheet names) and a README. They are ready for upload to a generalist
repository by a person. **No upload has been performed.**

## Limits
- One cancer type, one random sample. The 20% figure has a 95% confidence interval of roughly 16% to 25%.
- Dataset detection is size-based; a 40-row cohort table is real data but is counted as a "small table".
- Primary-versus-derived was judged by hand on 30 files, not across all 121.
- Two papers exceeded the download cap and 9 returned no files; they are counted as no dataset.
- Prior art: Gobeill et al. 2025 extracted 36 million supplementary files from all of PMC and indexed accession numbers
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC12371329/). PLOS and Springer Nature mirror new supplements to Figshare.
  Nobody has done funder-scoped, retrospective dataset classification, metadata, deposit, and catalogue listing.

---

# Full-population census (added 2026-09-23)

The pilot opened files from a 300-paper sample. The census read the full text of **every** paper in the population and
listed its attachments by filename, size and caption. No files were downloaded. Script: `census.py`; licenses via
`licenses.py`; summary in `data/census_summary.json`.

| Population: NCI-funded, open access, 2016-2022, has supplements, no repository accession | |
|---|---|
| Papers | 30,376 |
| Full text readable (1,427 returned server errors; can be retried) | 28,949 |
| Attachments listed | 89,820 |
| **Papers with >= 1 spreadsheet/CSV/TSV/TXT attachment** | **6,130 (21.2%)** |
| Papers with >= 1 Excel attachment | 5,870 (20.3%) |
| **Spreadsheet/CSV/TSV/TXT files** | **21,186** |
| Excel files alone | 19,818 (median 47 KB, 15.3 GB total) |
| Spreadsheet papers under CC BY or CC0 | 4,673 (76%) |
| Freely re-depositable spreadsheet/CSV files | 16,517 |
| Archive attachments (zip/gz/tar), not inspected | 3,203 |

Share of papers with a spreadsheet attachment is flat across years: 17% (2016) to 21-23% (2018-2022).
Top journals: Nature Communications 869, PLOS ONE 460, Scientific Reports 345, eLife 332, Oncotarget 215.

**Calibration against the pilot.** In the pilot, 70% of spreadsheet/CSV files met the dataset threshold and 79% of
spreadsheet-bearing papers had at least one such file. Applying those rates to the census:
about **14,800 dataset files in about 4,900 papers**, of which about **11,500 files are freely re-depositable**.
The two methods agree on the headline: 21% of papers by filename, 20% by opening the files.

**Caveats.** 4.7% of papers could not be read (server errors) and are excluded, so counts are slight undercounts.
Zip archives were not opened. "Dataset" is a size threshold, not a judgment of scientific value; about half of
rescued tables are derived results (see hand check above).
