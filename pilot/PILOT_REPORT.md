> **Read this first (2026-09-24).** The opening sections below are the original 2026-09-22 write-up and carry numbers that
> were later **corrected downward** after an independent methods review (population 30,376 → 26,228; "one in five" →
> 18.8% any / 14.5% native spreadsheet; 21,186 → 15,458 files). The current figures are in **"Corrections after an
> independent methods review"** and **"Three additions"** near the end, and in `data/census_summary_v3.json`,
> `data/four_cancers_v2.json`, `data/institutes.json`. The original text is kept so the change is auditable.

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

---

# Four-cancer replication (added 2026-09-23)

Same method as the glioblastoma pilot, three more cancer types, seed 20260923. Folders `data_breast_cancer/`,
`data_colorectal_cancer/`, `data_leukemia/`; summary in `data/four_cancers.json`.

| Cancer | Population | Sample | Papers with a dataset | Share | Native spreadsheet | CC BY / CC0 | Dataset files |
|---|--:|--:|--:|--:|--:|--:|--:|
| Glioblastoma | 630 | 300 | 61 | 20.3% | 46 | 46 | 121 |
| Breast cancer | 3,104 | 300 | 65 | 21.7% | 49 | 60 | 155 |
| Colorectal cancer | 888 | 300 | 67 | 22.3% | 51 | 58 | 157 |
| Leukemia | 1,272 | 300 | 63 | 21.0% | 46 | 43 | 148 |
| **Pooled** | | **1,200** | **256** | **21.3%** (95% CI 19.0–23.7%) | 192 | 207 (81%) | 581 |

The census (21.2% of papers have a spreadsheet attachment, by filename) and the pooled sample (21.3% have a
dataset-size table, by opening files) agree to within a tenth of a point. Applying 21.3% to the 28,949 readable
census papers gives about 6,170 papers; applying the observed 2.3 dataset files per paper gives about 14,000
files. The essay quotes the more conservative 11,000 to 12,000, derived from the census's 21,186 spreadsheet
files times the 70% of spreadsheet files that met the dataset threshold in the samples.

## Hand check, round two (added 2026-09-23)

45 more files from the breast, colorectal and leukemia samples (10 machine-positive and 5 machine-negative per cancer,
seed 77; list in `data/handcheck_sample2.json`), opened and judged by a person with `peek.py`.

- **30 files called "dataset": 30 are genuine data tables.** Roughly 13 primary (a 231-patient colorectal cohort
  table with stage, age, sex and disease-free survival; peptide hits; protein abundance; mutation tables; raw and
  normalized counts; a 5,000 × 99 phosphoproteomics matrix) and 15 derived (pathway enrichment, gene lists, Cox
  regression, dN/dS). Two are weak (a reagent list; a meta-analysis quality-assessment table in a PDF).
- **15 files called "not dataset": 12 correct.** The 3 misses were small results tables inside PDFs (17 and 20 rows;
  a one-page GEE estimates table; a GO-term list rendered as text), none of dataset size.
- One dataset appeared twice under two filenames in the same paper (Blood, PMC8532198), which is why the pipeline
  de-duplicates by content before deposit.

**Combined across both rounds (90 files: 45 + 45): 60 of 60 "dataset" calls were real data tables; of 30 rejections, 23 were
correct, 3 were missed small tables, 1 borderline, 3 unreadable; every miss was a table under 50 rows.** By content, about half of rescued tables are primary measurements
and half derived results.

---

# Corrections after an independent methods review (2026-09-23)

A methods reviewer re-derived every figure and found one real error and several softer problems. All are fixed
below, and the earlier sections above are left as written so the change is visible.

| | Before | After | Why |
|---|---|---|---|
| Population | 30,376 papers | **26,228** | The exclusion filter used `ACCESSION_TYPE:gen` (GenBank) and never excluded **GEO**. 4,150 papers with a GEO accession were wrongly included. Filter now excludes GEO too. |
| Sample: papers with a dataset (any file type) | 256 / 1,200 = 21.3% | **202 / 1,076 = 18.8%** | 124 sampled papers carried a GEO accession and are removed. PDF tables are no longer pooled across pages (earlier code merged unrelated small PDF tables into one "dataset"). |
| Sample: papers with a **native spreadsheet** dataset | not reported as primary | **156 / 1,076 = 14.5%** (95% CI 12.4–16.6%) | Reported as the primary figure; PDF/Word-only tables are secondary. |
| Per cancer (any / native) | 20–22% | glioblastoma 19.6 / 15.1 · breast 18.8 / 15.1 · colorectal 19.4 / 15.0 · leukemia 17.2 / 12.6 | Still within three points of each other. |
| Census: papers with a spreadsheet attachment | 6,130 (21.2%) | **4,759 (18.9%)** | Corrected population; includes 504 papers recovered on retry. |
| Census: spreadsheet/CSV files | 21,186 | **15,458** | Corrected population, plus a parser fix (below). |
| Freely licensed (CC BY / CC0) | 76% of papers | **80% of papers (12,738 files)**; 83% of sampled dataset papers | Unchanged in substance. |
| "Census and sample agree to a tenth of a point" | 21.2% vs 21.3% | **18.9% vs 17.9%** | Now a like-for-like comparison: both are "any spreadsheet attachment, by filename". The dataset-size rate by opening files is 18.8% any / 14.5% native. |
| Already mirrored on Figshare | "roughly one in five" (publisher pattern) | **13.5%** (27 of 200 random spreadsheet papers, same-paper match verified; all 27 are BMC/Springer Nature titles, no PLOS hit could be confirmed) | A raw filename search gave 40%, but generic names like `Table_1` matched unrelated items; only same-DOI or exact-title matches count. |
| Population filter validity | assumed | **15% of population papers point to a repository somewhere** (71 of 483: 50 with a data accession in the body text, mostly GSE/PXD/PRJNA/phs, that the text miner missed; 62 whose data-availability statement mentions a deposit repository or accession, 52 of them as the primary statement). 17% state the data is "in the paper/supplement"; 15% say "on request". `das_check.py`, `data/das_check_summary.json` | Folded into the estimate range. |
| Hand check | described in prose | **`data/handcheck_verdicts.csv`**: 90 files (45 + 45; earlier text said 105 in error), single rater (the AI assistant), not blind, machine fields visible. 58 clear + 2 weak real tables of 60 positives; of 30 negatives, 23 correct, 3 missed small tables, 1 borderline, 3 unreadable | Limitation stated; a second blind rater is the next step. |
| Threshold sensitivity (native, ≥3 cols) | not reported | ≥20 rows 15.9% · **≥50 rows 14.5%** · ≥100 13.1% · ≥200 11.6% · ≥1,000 rows 7.2% | The claim is not knife-edge on the threshold. |
| Census parser | `<media>` inside `<supplementary-material>` only | now every `<media>`/`<inline-supplementary-material>` in the article | Nature Communications "Source Data" and BMC "Additional files" use bare `<media>`; 6,891 papers from those publishers were rescanned. Attachments counted: 73,795 (was 72,450 before the parser fix on the same population). |
| Extrapolation arithmetic | "11,000–12,000 from 21,186 × 70%" (wrong: that product is 14,830) | see below | |

**Corrected estimate.** Start from 15,458 spreadsheet/CSV files in 4,759 papers. In the samples, 81% of
spreadsheet-bearing papers hold at least one dataset-size table and 70% of spreadsheet files meet the threshold.
Discount 15% for papers that do reference a repository somewhere and 13.5% for files already on Figshare.
That gives roughly **2,800 to 3,900 papers and 8,000 to 11,000 buried dataset files**, about three-quarters
under CC BY or CC0. The defensible headline is therefore **"roughly one in six such papers, on the order of
10,000 files,"** not "one in five, 21,000".

**Still open.** The four cancers were chosen for population size, not at random, so the pooled interval is
indicative rather than a strict population estimate. Only the open-access subset (about 36% of NCI papers)
was studied; author manuscripts are excluded and may behave differently. Zip archives were not opened.

---

# Three additions (2026-09-24)

**1. Rescued tables put back to work.** See `demo/README.md`. Three rescued glioma tables (PMC6478916, PMC8136167,
PMC6193287) joined by TCGA barcode: 244 shared patients, survival agrees within 0.5 month in 239, IDH in 236, age in
241. Pooled union of 1,037 patients with survival reproduces the IDH-mutant vs wildtype split (median 88 vs 15
months, log-rank p ≈ 6e-96). Cross-table: MARCO macrophage score (paper B) by DNA-methylation subtype (paper A),
n = 244, higher in Mesenchymal-like and LGm6-GBM than Classic-like. The third table is a 121-patient institutional
cohort with no other public home. Two of three tables derive from TCGA, so the survival result validates the data
rather than adding new biology.

**2. Patients, not files.** `data/patient_tables_verified.json`: ten patient-per-row tables opened and classified.
About 4,440 patient records after dropping PMC5499209 (GEO-flagged, 230 rows) and correcting table A to 812 rows; 523 (three tables) are institutional cohorts not found in TCGA, GEO, dbGaP or any catalogue.
The earlier keyword heuristic gave 7,034 rows across 25 tables; several of those were summary-statistics or
per-mutation tables, so only the verified figure is used.

**3. NIH-wide.** `institutes.py`, `data/institutes.json`. Same filename census (v2 parser, GEO-corrected filter),
random 300-paper samples, 2016–2022, open access, supplementary files, no accession:

| Institute | Population | Papers with a spreadsheet attachment |
|---|--:|--:|
| NHLBI | 16,339 | 44 / 295 = 14.9% |
| NIDDK | 12,954 | 52 / 295 = 17.6% |
| NIMH | 9,925 | 53 / 284 = 18.7% |
| NIA | 12,459 | 60 / 292 = 20.5% |
| NINDS | 11,366 | 67 / 281 = 23.8% |
| NCI (four-cancer samples, same yardstick) | 26,228 | 17.9% |

The five non-cancer populations total 63,043 papers. The pattern is a property of how biomedicine published
before 2023, not of cancer research.

---

# Gap-analysis follow-ups (2026-09-24, later)

- **BioStudies.** EMBL-EBI BioStudies holds one record per Europe PMC open-access article (accession `S-EPMC<pmcid>`,
  verified for PMC6193287: 4 files listed under the article title and abstract). It is a per-article file mirror with no
  dataset classification, per-file description, dataset identifier, or NCI catalogue entry. Added to prior art.
- **Catalogue-ready file.** `deliverable/ins_source_pmc_supplementary_datasets.tsv`: all 462 rescued datasets in the
  27-column schema of INS-Data's curated sources (header taken from `cedcd_datasets_curated.tsv`, release 2.4.1).
- **Plain-language descriptions** regenerated from column headers and sheet names for all 462 files (site and TSV);
  each states that it is automatically generated and not yet curated.
- **Buried-data index by journal.** `data/buried_index_by_journal.json`, 103 journals with ≥40 papers. Top by files:
  Nat Commun 3,201 (889 papers, 60%), eLife 1,440 (66%), PLoS One 1,052 (30%), Sci Rep 682 (14%), PLoS Genet 472 (51%).
- **Data-availability statements** (from `das_check`, 483 readable papers): 17% say data is in the paper/supplement,
  15% say available on request, 13% name a repository, 51% have no statement.
- **FAIR-SMART.** NLM's FAIR-SMART (Wei CH, Leaman R, Lai PT, Comeau D, Tian S, Lu Z. PLOS Biology 2025; PMID 41066526) aggregates PMC supplementary files, standardizes them to machine-readable form, LLM-categorizes tables, and serves them via API. Closest prior art; retrieval-oriented, no dataset identifiers, funder scoping, plain-language description, or catalogue listing. Added to Prompt 3.
- **Rules text.** FAQ: "For Track 1, a proposal to develop a mechanism for making outputs publicly available is explicitly responsive." Quoted in Prompt 1.
- **NOT-OD-26-100.** From 2026-10-01 recipients report data-sharing progress in RPPR C.5.c. Cited in Prompt 2 as the policy hook for a re-runnable per-grant census.
- **Post-2023 census.** `post2023.py`, `data/post2023.json`. Random 600 of the 10,874 NCI open-access papers published 2024–2025 with supplementary files and no repository accession: 139 of 599 (23.2%) carry a spreadsheet attachment (433 files). Higher than 2016–2022 (18.9%). The route the DMS policy was meant to close is still open. (2024 is under-represented in the open-access index: 62 of the 599 readable papers.)
- **Funding mechanisms.** `grants.py`, `data/mechanisms.json` (8,040 of the 26,228 population papers fetched before the run was stopped; 98% carry an NCI activity code). Share of papers acknowledging each mechanism family (papers can count in several): R01, R37, R35 investigator-initiated grants: 47.1%; P30 Cancer Center Support Grants: 44.9%; P50 SPOREs: 9.2%; P01 program projects: 8.4%; U01/U24/U54/UM1/U2C/U19 cooperative agreements and consortia: 17.6%; Training and career awards (T32, F, K, R25): 17.0%; R21, R03, R00, R50 small awards: 10.8%; Intramural (ZIA, ZIC, Z01; CCR and DCEG): 0.2%. Top codes: R01 3,584, P30 3,540, P50 724, P01 664, U01 632, R21 598, T32 562, U54 428, R35 220, U24 211, UM1 204, R00 151.


## Correction (2026-09-26): publisher Figshare deposits

A verification pass on the novelty claim found that **BMC/SpringerOpen deposit each "Additional file" to Figshare with its own
DOI, and PLOS deposits supporting information as one Figshare item per article**; those records reach the NLM Dataset Catalog and
Google Dataset Search. Our example cohort table (PMC6193287, `40478_2018_613_MOESM2_ESM.xlsx`) therefore already has DOI
10.6084/m9.figshare.7222268 and an NLM Dataset Catalog record, credited to the Burroughs Wellcome Fund with no NCI grant named.
By DOI prefix, BMC (10.1186) and PLOS (10.1371) account for about 23% of the files in the app index; the earlier "13.5%" was a
file-by-file confirmation that missed PLOS's article-level bundles. Nature Portfolio (10.1038, 40% of files), eLife, Elsevier
and Oncotarget deposit nothing (0 of 32 Nature Communications files matched). Figshare types files by extension, not content.
None of these records, Figshare-derived or otherwise, appears in the Index of NCI Studies, whose sources remain GEO, SRA,
dbGaP and curated NCI programs. Wording changed everywhere from "found in no catalogue" to the accurate statement; the net
estimate now discounts a fifth rather than 13.5% (7,000–11,000 files; 2,500–3,900 papers). DataMed was also found to be
effectively non-functional and is no longer cited as a live comparator.


**Update 2026-09-27:** grant fetch completed for all 26,228 population papers (98% carry an NCI activity code). Full-population mechanism shares: R01, R37, R35 investigator-initiated grants: 42.9%; P30 Cancer Center Support Grants: 46.7%; P50 SPOREs: 8.5%; P01 program projects: 7.2%; U01/U24/U54/UM1/U2C/U19 cooperative agreements and consortia: 19.0%; Training and career awards (T32, F, K, R25): 18.2%; R21, R03, R00, R50 small awards: 10.2%; Intramural (ZIA, ZIC, Z01; CCR and DCEG): 0.1%. `data/mechanisms.json` regenerated.


## Dollars and NIH-wide scale (2026-09-27)

`reporter_dollars.py`, `data/reporter_dollars.json`, `data/dollars_summary.json`. The 4,759 census papers with a spreadsheet attachment acknowledge **4,242 distinct NCI core projects**; NIH RePORTER parent-award totals for FY2016–2022 sum to **$11.21 billion** (3,433 grants had award rows in that window). Largest: U10CA180886 CHOP $197M (NCTN), U10CA180821 BWH $98M, P30CA008748 MSK $98M, U10CA180868 NRG $97M, P30CA006516 Dana-Farber $90M, P30CA016672 MD Anderson $82M. This is the funding *behind* the papers, not the cost of the datasets; grants fund many outputs. NIH-wide population (same filter, all 24 institutes, 2016–2022): 124,758 papers; at the measured 15–24% spreadsheet rate and 70% dataset threshold, on the order of 50,000 buried dataset files across NIH.


## Full-corpus classification (2026-09-28)

`data_full/`: every attachment of the 4,759 census papers with a spreadsheet was downloaded (4,673 retrieved; 86 over the
120 MB cap) and classified with the same classifier as the samples. **25,411 files; 9,543 dataset files in 3,736 papers**
(14.9% of the 25,138 readable population papers, matching the samples' 14.5% native-spreadsheet rate). 7,990 primary,
1,553 derived; 8,123 (85%) CC BY or CC0. By DOI prefix, 2,208 are in BMC or PLOS papers (publisher Figshare deposit),
leaving **7,335 with no identifier anywhere**; 3,793 are Nature Portfolio. Largest table 1,321,526 rows. The estimate
ranges above are superseded by this measurement. The INS deliverable now holds all 9,543 rows; the app marks every
classified file.


## Blind human check (2026-09-29)

`human_check/`: 30 files drawn at random from the full-corpus classification (seed 20260929; 15 machine-positive, 15
machine-negative, order shuffled), extracted locally and judged by the submitter without access to the machine labels
(`key_do_not_open.json`). Answers in `answers_2026-09-29.json`, score in `score.json`.
**26 of 30 agree (90%); Cohen's kappa 0.79.** Machine-positive: 13 agreed, 1 judged not a dataset (#30, a 74-row cell-type
proportion table), 1 unsure (#26, a 98-row commercial PCR-array list that would not open; likely a machine false positive).
Machine-negative: 13 agreed, 2 judged real (#2, #12: tables of 43 and 44 rows, just under the 50-row threshold). The
classifier errs toward the conservative side, so 9,543 is a floor rather than an overcount.


## Second blind human check (2026-09-30)

`human_check_2/`: 30 new files (no overlap with set 1; seed 20260930; 15 machine-positive, 15 machine-negative, shuffled;
.xls excluded after set 1's unreadable file), judged by hand without the machine labels. **28 of 30 agree (93%; kappa 0.87).**
Disagreements: #14 (44-row table, machine rejected, rater real) and #29 (53-row pathway-result list, machine real, rater not).
**Combined with set 1: 54 of 60 agree (90%; kappa 0.83 over the 59 judged).** In 3 of the 5 disagreements the machine was
stricter. A re-answer of set 1 made after its disputed items had been discussed in the working session is excluded, because
it was not blind (`human_check/answers_J_same_set.json`, kept for the record).


## Dollar figure correction (2026-09-30)

The essay attributed $11.2B to the papers the 9,543 datasets come from; $11.2B (4,242 grants) is for all 4,759 spreadsheet papers. For the 3,736 papers that hold a dataset, the grants number 3,598 and their FY2016–2022 parent awards total **$10.27B**. Essay, evidence sheet and site now use $10.3B.
