# Reuse demonstration: rescued tables put back to work

Three supplementary spreadsheets rescued in the glioblastoma sample (two hold pan-glioma TCGA cohorts, one an institutional glioma cohort), none of them listed in any data catalogue,
were combined into analyses that none of the three source papers performed. Script: `pooled_glioma.py`.
Outputs: `figure.png`, `pooled_cohort.csv`, `join_stats.json`. Everything runs from the public files once `rescue_pilot.py fetch` has downloaded the glioblastoma sample (the zips are not in the repo).

| Table | Source | What it holds |
|---|---|---|
| A | Commun Biol 2019, PMC6478916, Supplementary Data 1b | 812 TCGA glioma patients: IDH-codel subtype, DNA-methylation subtype, overall survival, vital status, age, grade |
| B | Genome Med 2021, PMC8136167, sheet F2C-D | 603 TCGA glioma patients: MARCO macrophage expression score, overall survival, death, MGMT, IDH |
| C | Acta Neuropathol Commun 2018, PMC6193287 | 121 patients from one hospital's own cohort: IDH/TERT status, MGMT, ATRX, follow-up status. Not found in TCGA, GEO, dbGaP or any catalogue. |

## What the join shows

1. **The tables really describe the same people.** A and B share 244 TCGA barcodes. On those 244, overall survival
   agrees to within half a month in 239, IDH status in 236, age in 241. Rescued tables from different papers can be
   joined reliably by a public identifier, which is the precondition for cataloguing them as datasets.
2. **A pooled cohort of 1,037 patients with survival, assembled only from rescued files, reproduces the field's
   best-known result.** Median survival 88 months for IDH-mutant versus 15 months for IDH-wildtype glioma
   (log-rank p < 1e-90). This is a validation, not a discovery: it shows the rescued data is fit for purpose.
3. **A cross-table analysis neither paper could do alone.** Paper B measured a macrophage score; paper A assigned
   DNA-methylation subtypes. Joined, MARCO is higher in Mesenchymal-like and LGm6-GBM tumours than in Classic-like
   ones (n = 197 with both values and a subtype group of at least 8). Modest, but it exists only because two buried files were put side by side.
4. **An institutional cohort that would otherwise be lost.** Table C is 121 real patients with molecular status and
   outcome from a single hospital, not found in TCGA, GEO, dbGaP or any catalogue. Its status column groups tumours as
   "IDH or TERT mutated" versus "double wild-type", which is a different axis from the IDH split above, and follow-up
   time is not given. 4 of 16 double wild-type versus 18 of 105 mutated patients were deceased at follow-up: too small
   to interpret, shown descriptively only.

## Why this matters for the proposal

The rescue pipeline's value is not that the files exist, but that they can be found, joined and used. This
demonstration took an afternoon once the files were located; locating them without the census would have required
already knowing three specific papers. Tables A and B are curated slices of public TCGA data; table C is primary
clinical data. Across the four cancer samples, verified patient-level tables describe about 4,400 patient records,
of which about 500 come from institutional cohorts not found in any catalogue (`pilot/data/patient_tables_verified.json`).

Limits: two of the three tables derive from TCGA, so the survival result is a reproduction of known biology, not
new evidence about glioma. The MARCO-by-subtype comparison is descriptive and unadjusted. No patient-identifying
information is present in any file; all three were published open access under CC BY.
