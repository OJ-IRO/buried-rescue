# Attachment Rescue: finding the cancer data NCI already paid for

**Track 1 (Ideas). Draft v5, 2026-09-29. Not submitted.** Detailed figures and methods are on the Supporting Evidence page and in `pilot/PILOT_REPORT.md`.

---

**In brief.** We checked about 26,000 NCI-funded papers, opened all 25,000 attachments of those carrying spreadsheets, and found 9,543 hidden datasets, 7,335 of them with no permanent link, from papers crediting $10.3 billion in NCI grants. We have already built the fix, a public search tool, and a file NCI's own catalogue can load today. See it at [attachment-rescue.vercel.app](https://attachment-rescue.vercel.app).

<!--FIG-->

## Prompt 1: Significance and Approach

**The problem.** For years, when cancer scientists published a paper, they shared their data by attaching a spreadsheet to it, usually labelled something like "Supplementary Data 3." Patient records, gene measurements, drug test results: all of it went into attachments. Those files still exist. But no data catalogue lists them, no search engine looks inside them, and nothing tells a researcher what they contain. The only way to find one is to already know which paper to open.

One example: a hospital published a table of 121 brain tumor patients in 2018, with each patient's tumor type and genetic markers, exactly what a brain cancer researcher might need. It sits in an attachment. The publisher did give it a permanent link, yet that record names a different funder, and NCI's own catalogue has never heard of it. Unless you already know that paper exists, you will never find this data.

**How big is it?** We did not guess. We checked every NCI-funded paper from 2016 to 2022 that is free to read and has attachments but does not point to a data repository. That is about 26,000 papers. For the 4,759 of them with a spreadsheet attached, we downloaded and opened every attachment, about 25,000 files.

We only counted a file as a real dataset if it was big enough for someone to reuse, not just the few numbers behind one chart. Even with that strict rule, we found:

- **9,543 real datasets**, hidden in about one in seven of those papers.
- **7,335 of them have no permanent link of their own.** Nobody can reliably cite them or find them.
- The papers they come from credit NCI grants worth **$10.3 billion** (2016 to 2022 awards).

To test our sorting program, we ran two blind checks in which 60 random files were judged by hand, without seeing the program's answers. They agreed with the program on 54 of 60. In most of the disagreements the program had been the stricter one, rejecting tables just short of our size rule, so if anything our count is low.

**It is still happening.** In 2023, NIH introduced a new policy asking scientists to share data properly. But when we checked papers from 2024 and 2025, nearly a quarter still attached spreadsheets instead of putting their data in a proper repository. The problem did not stop. If anything, it is more common.

**Who this hurts.** Researchers and clinicians lose data they could build on; students, small labs, and newcomers lose most, lacking the connections that point to the right paper. Patients lose too: the hidden tables in our samples alone describe about 4,400 patients, including about 500 from hospital studies that are not in the major public cancer databases. Authors lose credit, because data without a permanent link cannot be cited. And NCI loses the return on research it already paid for.

**Why this matters to NCI's goals.** The scientists behind these papers followed the norms of their time, and the data still disappeared from view. That is what this challenge means when it says policy alone does not change culture. The Office of Data Sharing has named missing descriptions and hard-to-find data as major barriers. An attachment is the clearest example of both: real data with no description, sitting where no one looks. It also cuts against NCI's commitment to broad, rapid, and equitable sharing. Data that only insiders can find is not broadly shared, it reaches people slowly if at all, and it favors well-connected labs over everyone else. The challenge also says that, for this track, a way to make research outputs publicly available is "explicitly responsive." This is that way.

**Our solution.** We call it Attachment Rescue. It has six steps, and every tool it needs already exists:

1. **Find** the papers that shared data only as attachments.
2. **Sort** the attachments into real datasets and everything else.
3. **Describe** each dataset in plain English: what it is, who made it, and which grant paid for it.
4. **Give it a permanent link**, by placing a copy in a free public repository that NIH already recognizes. If copying is not allowed, we link to the original instead.
5. **List it in NCI's own catalogue**, the Index of NCI Studies, so researchers can search for it.
6. **Keep it alive** by checking every link each month.

**We already did most of it.** Steps 1 to 3 have been done for every NCI paper we checked. We built a file with all 9,543 datasets in the exact format NCI's catalogue already uses, so adding them is a single upload. We also built a free public search tool, [attachment-rescue.vercel.app/app](https://attachment-rescue.vercel.app/app), where anyone can look up a paper or an NCI grant and see what data it left behind.

**Intended outcomes.** Every hidden NCI dataset gets a description, a permanent link, and a place in NCI's catalogue; NCI gets a running count of what its grants have shared; and new papers are caught as they appear.

And we showed the rescued data works. We joined two hidden tables from two different papers into one group of 1,037 patients, and the combined data gave the right answer to a well-known question about brain tumor survival. These files are usable science.

## Prompt 2: Potential Impact on the Cancer Research Community

**Right away.** Thousands of cancer datasets that already exist become searchable, citable, and described. No new experiments, no new data collection. A researcher who can find an existing patient cohort in minutes, instead of never, can test an idea months sooner. That speeds up cancer research, expands access to outputs NCI already funded, and makes each file more useful by describing it.

**Far beyond one program.** This is not only a cancer problem. Five other NIH institutes we checked, covering heart, diabetes, mental health, aging, and brain research, show the same pattern, and about 125,000 papers across NIH fit it.

**For people who are not data experts.** Every rescued dataset comes with a plain-English description and a permanent link. A community college teacher could hand students a real patient table; a student team could search for "patients with survival data" and find something. We propose sharing the rescued collection at NCI's Data Jamboree in November 2026, an event built for exactly these users.

**For scientists.** Data with a permanent link can be cited, and papers with linked data tend to be cited more.

**For NCI's leaders.** For the first time, NCI can see how much of its own funded data is hidden, broken down by year, by journal, and by grant. The hidden data comes from every part of NCI's funding, so it matters across NCI's Divisions, Offices, and Centers: the Cancer Centers Program (almost half of these papers credit a cancer center grant), the clinical trial networks, the research divisions that fund individual grants, and the training programs. Each can see its own share. Our tool can already answer a question like "what data did this cancer center's grant leave behind?" Starting in October 2026, NIH requires grant holders to report on their data sharing in their yearly progress reports. Our check gives program staff an independent way to see what was actually shared.

## Prompt 3: Innovation and Awareness of Existing Efforts

**What already exists.** The pieces exist, but no one has put them together this way.

- **Tools that read attachments for computers.** The National Library of Medicine's FAIR-SMART system (2025) collects these attachments and sorts their tables so computer programs can search them. A Swiss team (2025) made 36 million attachments searchable by keyword. They are built for machines and searches. They do not decide which files are real datasets, give them permanent links, or put them in NCI's catalogue. FAIR-SMART would make a good starting point for our work, not a replacement.
- **Some publishers already give files permanent links.** BMC and PLOS copy their attachments to Figshare, which gives each a permanent link, covering about a fifth of the datasets we found. Those records carry the publisher's details, which can leave NCI uncredited, as with our brain tumor example, and none appear in NCI's catalogue. Other publishers, including Nature journals, which hold the largest share, do nothing like this.
- **Research on the problem.** Earlier studies found most papers point to attachments rather than repositories, and that permanent links outlast ordinary web links.
- **NCI's own catalogue.** The Index of NCI Studies collects datasets from major repositories and already uses automated tools to improve its records, but collects nothing from attachments. Adding one source is a natural next step, not a new system.

**What is new.** Attachment Rescue is a novel combination of existing tools, applied in a new context: one funder's own published record. Other projects help computers search papers. Ours does three things none of them do.

1. **We measured NCI's own blind spot.** Not "data is hard to find" in general, but a count: NCI grants worth $10.3 billion produced papers holding 9,543 datasets, and 7,335 of them have no permanent link of their own. We could find no one who has counted this for any funder before. We also showed it is still happening today, and that every NIH institute we checked has the same problem.
2. **The work is already done, not just proposed.** We opened all 25,000 attachments. We proved the rescued data works by combining it into a 1,037-patient result. We built the file NCI's catalogue can load right now. And we put up a live tool where anyone, including a program officer, can type in a grant number and see what data it left behind.
3. **It is built for NCI.** Other systems serve search engines and programmers. Ours answers the questions NCI's own staff ask: what did our grants produce, where is it, and how do we get it into our own catalogue? And the fix costs almost nothing.

In short: others describe the problem. We measured it for NCI, prepared the fix for every paper, and are handing NCI the result.

**What we are not proposing.** No new repository, no new catalogue, and no replacement for NIH's 2023 policy. Attachment Rescue fills in what came before it and catches what still slips through.

## Prompt 4: Transferability, Sustainability, and Feasibility

**How NCI could adopt it.** Every part already exists: the papers are public, free repositories give out permanent links, and NCI's catalogue already accepts new sources. Adopting Attachment Rescue means adding one source. It is a decision, not a construction project.

**What it would cost.** Very little. Our whole run, checking 26,000 papers and opening 25,000 files, took about two days on one laptop. The main human cost is spot-checking descriptions: at about a minute per dataset, the full backlog is roughly 160 hours, or about a tenth of one staff member's year. The catalogue file is already built.

**Partners needed.** Three, all already part of NIH's data ecosystem: NCI's catalogue team at CBIIT, to add the new source; one of the free general-purpose repositories in NIH's Generalist Repository Ecosystem Initiative, to hold copies and issue permanent links; and, optionally, the National Library of Medicine's FAIR-SMART team, whose file conversion could replace ours.

**How others can adopt or adapt it.** The same steps work for any funder or institution by changing one search setting. Another NIH institute can run it on its own grants. A university library can run it on its own researchers' papers. A journal can run it on its back catalogue. Our code and instructions are public at [github.com/OJ-IRO/attachment-rescue](https://github.com/OJ-IRO/attachment-rescue).

**Honest limits and how we handle them.**

- **Permission to copy.** Most of these papers, about four in five, use open licenses that allow copying. For the rest, we link to the original instead of making a copy.
- **Respecting authors.** No one should upload other people's files without telling them. The best option is for NCI to act as the official uploader, the way NIH already handles its own staff's papers. Otherwise, authors get 60 days' notice and a simple way to say no. If they say no, we only link to their file. Either way, the original authors are always credited, and any table about patients gets an extra review before it is copied.
- **Not every table is equally useful.** Some are analysis results rather than raw measurements; each record says which.
- **Avoiding duplicates.** Where a file was also shared elsewhere or already has a publisher's link, we reuse that link.
- **The one outside decision.** NCI's catalogue team must agree to add the source. If they do not, the datasets still get permanent links, and our count still stands.

**How it lasts.** It persists because it lives inside a system NCI already maintains: the catalogue has regular releases, and rescue becomes one more source in each release. After the backlog, it checks new papers every three months and every link monthly, automatically. The new progress-report rule gives NCI a standing reason to keep it running. The file and full count are public, so any funder can use it as a model.

## Use of Generative AI

We used generative AI (Anthropic's Claude) to help write and run our analysis code, draft and edit this narrative, and draft the dataset descriptions. Every number comes from our scripts, which anyone can rerun on public data. No controlled-access NIH data was used; every file analyzed is open access. The two blind checks of 60 files were done by hand, without seeing the program's answers; an earlier check of 90 files was done with the AI assistant. All are published so others can review them. All decisions about what to claim and recommend are the submitter's own, and the submitter takes full responsibility for the content.
