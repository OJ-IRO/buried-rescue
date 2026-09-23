# NCI ODS Impact Prize, Track 1: what a winning entry looks like

Written 2026-09-21. Deadline 2026-10-05, 11:59 PM ET (14 days).
Every data figure below is reproducible with `verify_findings.py` in this folder, using only the public
Index of NCI Studies (INS) release 2.4.1. Web claims carry their source. Items I could not confirm are marked UNVERIFIED.

## 1. Bottom line

The team's core observation is real and reproduces exactly. The current draft built on it would probably not place,
because a skeptical NCI reviewer can knock down its main evidence in about five minutes using NCI's own website.
All of the holes are fixable inside two weeks, and the repaired idea is stronger, simpler, and closer to what this
office has said in print that it wants.

Keep: the measured gap, the honest negative result, the "your own tools, one table over" tone.
Change: what the fields should be, who the policy ask is aimed at, and the evidence behind the AI claim.

## 2. What is wrong with the current draft (all verified against the data)

| # | Problem | Evidence | Severity |
|---|---|---|---|
| 1 | The draft says users cannot tell a 12-person study from a 1,200-person one. INS already shows a sample count for 100% of GEO records, on the website. The draft never mentions it. | verify_findings.py section 1 | Fatal if left |
| 2 | The pilot's headline (96% within tenfold) is matched by a free guess. Assuming participants = sample count scores 95.3% within tenfold across 1,028 dbGaP records, and 96% / 28% exact on the pilot's own 50 records. The AI scored 96% / 30%. | section 2 | Fatal if left |
| 3 | The draft states `primary_disease` "sits at 100%". For all 7,675 GEO records the value is the hard-coded string "Not Reported". This is a factual error in a cancer index whose website has only two filters, one of which is disease. | section 5; CBIIT/INS-Data `modules/gather_geo_data.py` line 854 | High |
| 4 | "12,620 datasets" double counts. 93% of SRA records share an exact title with a GEO record. Distinct open studies: about 7,900. | section 4 | High |
| 5 | Many open records have no human participants at all (mouse, cell line). "Participant count" is not applicable to them, and the pilot was validated only on human cohort studies. | section 6 (crude keyword scan, indicative only). A background review reported 61% of GEO records as human-only, but the INS files have no organism column and I could not reproduce that figure. UNVERIFIED | High |
| 6 | "Collect reuse limitations at deposit" is aimed at the wrong agency and is mostly redundant. GEO and SRA belong to NCBI/NLM, not NCI. GEO's own FAQ: "GEO is an unrestricted-access database." For most open records the correct value is simply "none". | https://www.ncbi.nlm.nih.gov/geo/info/disclaimer.html ; archived GEO FAQ 2026-08-13 | High |
| 7 | Pilot is n=50, run by hand, confidence intervals overlap the baseline. | repo research note 2026-09-03, section 4 | Medium |
| 8 | The essay headings and content miss things the prompts explicitly ask for (section 5 below). | archived challenge page, 2026-09-13 | Medium |

Problem 6 also explains the pilot's "no signal" consent result: open records have no consent class to infer.

## 3. The repaired idea

Working title: **"Three facts before you download: making the open two-thirds of NCI's study index appraisable."**

For every open-deposit record in INS, publish three plain facts that a non-specialist needs before committing a week to a dataset.

1. **Does it contain human participants?** Human tissue, cell line, or model organism.
   Mostly a lookup: GEO's public API already returns the organism. Text is needed only to split human tissue from human cell lines.
2. **How many people, not how many samples?** Only for human-participant records, shown as an estimate with its error rate.
   The argument is now grounded in NCI's own data: where both numbers are known, samples equal participants only 25% of the time
   and differ by 2x or more in 52% of records. Live examples exist in INS today, such as GSE296535, listed with 6 samples
   and described as 678 patients.
3. **What is the true access situation?** Three values: open; open processed data with controlled-access raw data (linked to its dbGaP study);
   controlled. For dbGaP records, express the existing consent codes in the international Data Use Ontology standard using the
   mapping already published by Lawson et al. 2023 (98% of NCI limitations mappable). INS currently links none of these pairs,
   yet 65 publications are shared between an open record and a dbGaP record, and about 20 open records say outright that their raw data sits in dbGaP.

Plus three housekeeping fixes that need no AI at all, which make the proposal look practical instead of ambitious:
- Fill SRA size from NCBI's public API. All 4,945 SRA records currently show no size of any kind. I tested the call; it works.
- Link the 93% of SRA records that duplicate a GEO record, using the SRA link GEO's API already returns.
- Show "not collected by the source repository" instead of silently hiding blank fields. INS release notes confirm the blanks are currently hidden from display.

**Keep the negative result, reframed.** "We tried to infer consent class from text and got exactly the majority-class baseline.
Do not guess this field. Where a controlled-access twin exists, inherit its terms by link. Where none exists, say 'open by repository policy'."
That is still the most credible paragraph in the essay.

**Aim the policy ask at levers ODS actually holds:**
- NCI's data management and sharing plan guidance and template: ask depositors to state the number of human participants in the GEO summary
  and to cross-reference the dbGaP accession when raw data is controlled.
- The INS schema and pipeline, which ODS manages.
- The Cancer Research Data Commons submission portal.
Name NCBI ownership of GEO and SRA as a known constraint. Prompt 4 asks for exactly that.

**Do not propose filling the disease field.** NCI is already building an AI disease mapper (github.com/CBIIT/ccdi-ins-icdo-mapping-llm,
last pushed 2026-06-22). Cite it instead: it proves the INS team already runs this kind of enrichment, so the three facts slot into
an existing pipeline. That is the strongest possible adoption argument.

## 4. What wins contests like this (evidence from past federal prizes)

Closest comparable: the NIH S-index Challenge, whose first round in 2025 was an ideas round on data sharing. Seven winners at $15K.
A two-person ecology consultancy placed alongside Harvard and Yale. The eventual $400K winner called its own idea "simple"
and arrived with a working public prototype. Judged on "originality, technical feasibility, real-world impact, and clarity".
Source: https://www.nei.nih.gov/research-and-training/research-news/nih-announces-winners-s-index-challenge-advance-data-sharing-across-biomedical-research

The DataWorks! Prize (NIH and FASEB, 2022 to 2024) shows the same pattern. Big consortia took the top prizes, but every cycle
a small, practical, burden-reducing entry won a lower tier: a university library's file-naming worksheet, a single lab's methods for
repairing missing metadata. Source: https://www.faseb.org/data-management-and-sharing/dataworks-prize/2022-dataworks-prize-winners

Traits the winners share, and where the repaired idea stands:

| Winning trait | Status |
|---|---|
| Quantifies the gap with the sponsor's own data | Yes, strongly |
| Simple enough to explain in two sentences | Yes after the rewrite |
| Working public prototype, even in an ideas round | Not yet. Needs a public repo and an output file (section 6) |
| Adoption through existing infrastructure, not a new platform | Yes. INS pipeline plus NCI's existing AI disease mapper |
| Reduces burden on researchers | Yes |
| Clear writing for non-specialist federal staff | Draft is dense. Needs a plain-language pass |
| Small and unconventional teams can place | Yes, and the organizer said on record they want outsiders |

Competition signals: public engagement with the prize looks low. The one public competing entry I found
(github.com/woahwhattheheck/commons issue 14017, a "Reuse Receipt" metadata convention) is generic, not cancer specific,
run largely by automated agents, and on hold. Expect other entrants to quote the same NCI statistics about reuse and attribution
(60% of shared datasets reused, 18% without credit). Do not lead with those.

## 5. What the judges have said in print that they care about

The judges are NCI program staff, and the ODS team has published its own diagnosis. Quoting it back, accurately, is the cheapest points available.

- "Findability of siloed data was identified as a major bottleneck" and participants "expressed concern ... due to incomplete, incorrect, or missing metadata."
  They suggested data tables that "quickly highlight missing information". Ghosh et al., JNCI, Dec 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12782234/
  The same paper names the Index of NCI Studies as a key exemplar "managed by NCI ODS". INS is the judges' own product.
- Researchers "often prefer to rely on their own datasets due to concerns about data quality and trust." Boja et al., JCO Clinical Cancer Informatics, Aug 2026.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC13479720/
- ODS describes "user-centered processes for cancer data access and submission." Boyd et al., JNCI 2026 (first author runs this prize).
  https://academic.oup.com/jnci/advance-article/doi/10.1093/jnci/djag199/8719042
- NIH Strategic Plan for Data Science 2025 to 2030: help investigators "find and appraise the relevance" of data, and "enhance automated ... curation processes."
- The NCI Data Jamboree on 2026-11-16 lists INS first among its data discovery entry points and says "Computational expertise is not required."
  Those participants are exactly who hits these blanks. https://events.cancer.gov/nci/datajamboree/resources
- NCI Director Letai, the prize's approving official, on AI: "shared and interoperable."

Avoid: framing INS as deficient (the blanks are a deliberate design choice, so call this the next maturity step); equity language beyond the prize's
own phrase "broad, rapid, and equitable"; any AI processing of controlled-access data (NIH notice NOT-OD-25-081 restricts it; use public metadata only);
arguments about international access; proposals needing new curation staff.

**Exact prompt wording the draft does not yet answer** (from the archived challenge page):
- Prompt 1 asks "who is affected by it (for example, researchers, patients, clinicians, institutions)" and "How the gap aligns with NCI's commitment to broad, rapid, and equitable sharing".
- Prompt 2 is titled "Potential Impact on the Cancer Research Community" and asks about "cross-cutting practice, policy, or infrastructure across NCI's Divisions, Offices, and Centers (DOCs)". The draft never mentions them.
- Prompt 4 asks for "any known constraints in policy, infrastructure, community practice, or resources". NCBI ownership of GEO and SRA is the honest answer.
Use the four prompt titles verbatim as headings.

## 6. Two-week plan

| When | Task | Who | Hours |
|---|---|---|---|
| Days 1 to 2 | Decide whether to adopt the repaired idea. Email ODS one scope question if any remains. | Ian, Jay | 1 |
| Days 2 to 6 | Build a real validation set: 300 GEO records sampled across human tissue, cell line, mouse, and single-cell studies. Two people label each from the linked paper: human-participant yes or no, and number of people. Report agreement between labelers. | Ian and Jay independently | 10 to 12 |
| Days 4 to 7 | Run three methods on it through the API with saved prompts: sample count as a guess, a text pattern match, and the AI. Report exact and within-2x accuracy, not within-tenfold. Report cost per record. If the AI does not beat the free guess on human-tissue records, say so and narrow the claim. | Ian | 4 |
| Days 5 to 8 | Publish a public repo: the completeness report, the duplicate and linkage audit, the validation set, and a sample output file of the three facts for a few hundred records. Open license. | Ian | 3 |
| Days 7 to 10 | Rewrite the essay around the three facts. Verbatim headings. Plain-language pass. Count words in the final PDF. | Ian | 6 |
| Days 8 to 10 | One-page Supporting Evidence PDF: asymmetry table, samples-versus-people chart, two live examples, validation table, links, license. | Ian | 2 |
| Days 10 to 12 | Review against the four criteria. Optional 30-minute read by a cancer data person. | Jay | 3 |
| Day 12 | Download and sign the registration form. A person sends the email. Leave two days of slack for a corrected resend. | Human | 1 |

The labeling is the step that turns this from an interesting observation into evidence. It is also the only step that cannot be compressed.

## 7. Honest odds

Five Track 1 prizes plus a shot at the grand prize. Unknown number of entrants; signals suggest a modest field.
The repaired entry would have measured evidence from the sponsor's own flagship product, a working public artifact, a negative result,
and an adoption path through a pipeline NCI already runs. Few ideas-round entries will have any of those. The main remaining weakness
is no cancer-domain voice on the team, which the rules say cannot be scored against you.
As it stands today, the draft carries a factual error and a headline result that a free guess matches. I would not send it unchanged.

## Could not verify
- The judging panel's membership and the expected number of submissions.
- Whether any 2025 to 2026 AI curation paper already publishes study-level donor counts for GEO. The skeptic found none in MetaSRA or MetaHQ, but did not read every recent paper.
- Whether dbGaP itself now serves Data Use Ontology codes directly.
- The human versus non-human split in section 2 rests on keyword scans and the organism field, not on hand curation. The 300-record labeling would settle it.
