# Attachment Rescue: finding the cancer data NCI already paid for

**Track 1 (Ideas). Draft v5, 2026-09-29. Not submitted.** Detailed figures and methods are on the Supporting Evidence page and in `pilot/PILOT_REPORT.md`.

---

**In brief.** We checked about 26,000 NCI-funded papers, opened all 25,000 attachments of those carrying spreadsheets, and found 9,543 hidden datasets, 7,335 of them with no permanent link, from papers crediting $11.2 billion in NCI grants. We have already built the fix, a public search tool, and a file NCI's own catalogue can load today.

<!--FIG-->

## Prompt 1: Significance and Approach

**The problem.** For years, when cancer scientists published a paper, they shared their data by attaching a spreadsheet to it, usually labelled something like "Supplementary Data 3." Patient records, gene measurements, drug test results: all of it went into attachments. Those files still exist. But no data catalogue lists them, no search engine looks inside them, and nothing tells a researcher what they contain. The only way to find one is to already know which paper to open.

Here is one example. A hospital published a table of 121 brain tumor patients in 2018, with each patient's tumor type and genetic markers. It is exactly what a brain cancer researcher might need. But it sits in an attachment. The publisher did give it a permanent link, yet that record names a different funder, and NCI's own catalogue has never heard of it. Unless you already know that paper exists, you will never find this data.

**How big is it?** We did not guess. We checked every NCI-funded paper from 2016 to 2022 that is free to read and has attachments but does not point to a data repository. That is about 26,000 papers. For the 4,759 of them with a spreadsheet attached, we downloaded and opened every attachment, about 25,000 files.

We only counted a file as a real dataset if it was big enough for someone to reuse, not just the few numbers behind one chart. Even with that strict rule, we found:

- **9,543 real datasets**, hidden in about one in seven of those papers.
- **7,335 of them have no permanent link of their own.** Nobody can reliably cite them or find them.
- The papers they come from credit NCI grants worth **$11.2 billion** (2016 to 2022 awards).

To test our sorting program, a person who was not told its answers checked 30 random files by hand. They agreed on 26 of 30. In two of the three disagreements, the program had been the stricter one, rejecting tables just short of our size rule. So if anything, our count is low.

**It is still happening.** In 2023, NIH introduced a new policy asking scientists to share data properly. But when we checked papers from 2024 and 2025, nearly a quarter still attached spreadsheets instead of putting their data in a proper repository. The problem did not stop. If anything, it is more common.

**Who this hurts.** Researchers lose data they could build on. Students, small labs, and newcomers lose most, because they do not have the connections that tell them which paper to open. Patients lose too: the hidden tables in our samples alone describe about 4,400 patients, including about 500 from hospital studies that are not in the major public cancer databases. Authors lose credit, because data without a permanent link cannot be cited. And NCI loses the return on research it already paid for.

**Why this matters to NCI's goals.** The scientists behind these papers did nothing wrong. They followed the norms of their time. The data still disappeared from view. That is exactly what this challenge means when it says policy alone does not change culture. The Office of Data Sharing has itself named missing descriptions and hard-to-find data as major barriers. An attachment is the clearest example of both: real data with no description, sitting where no one looks. The challenge also says that, for this track, a way to make research outputs publicly available is "explicitly responsive." This is that way.

**Our solution.** We call it Attachment Rescue. It has six steps, and every tool it needs already exists:

1. **Find** the papers that shared data only as attachments.
2. **Sort** the attachments into real datasets and everything else.
3. **Describe** each dataset in plain English: what it is, who made it, and which grant paid for it.
4. **Give it a permanent link**, by placing a copy in a free public repository that NIH already recognizes. If copying is not allowed, we link to the original instead.
5. **List it in NCI's own catalogue**, the Index of NCI Studies, so researchers can search for it.
6. **Keep it alive** by checking every link each month.

**We already did most of it.** Steps 1 to 3 have been done for every NCI paper we checked. We built a file with all 9,543 datasets in the exact format NCI's catalogue already uses, so adding them is a single upload. We also built a free public search tool, where anyone can look up a paper or an NCI grant and see what data it left behind.

And we showed the rescued data actually works. We took two hidden tables from two different papers and joined them into one group of 1,037 patients. The combined data gave the right answer to a well-known question about brain tumor survival. That tells us these files are not junk. They are usable science.

## Prompt 2: Potential Impact on the Cancer Research Community

**Right away.** Thousands of cancer datasets that already exist become searchable, citable, and described. No new experiments, no new data collection. The work is already done; it just needs to be found.

**Far beyond one program.** This is not only a cancer problem. We ran the same check on five other NIH institutes, including heart, diabetes, mental health, aging, and brain research. All of them show the same pattern. Across all of NIH, about 125,000 papers fit it. Our method works for any institute, or any part of NCI, by changing a single search setting.

**For people who are not data experts.** Every rescued dataset comes with a short plain-English description and a permanent link. A community college teacher could hand students a real patient table. A student team could search the catalogue for "patients with survival data" and actually find something. We propose sharing the rescued collection at NCI's Data Jamboree in November 2026, an event built for exactly these users.

**For scientists.** Once their data has a permanent link, it can finally be cited. Research suggests papers with linked data get cited more. Authors would get that benefit without lifting a finger.

**For NCI's leaders.** For the first time, NCI can see how much of its own funded data is hidden, broken down by year, by journal, and by grant. The hidden data comes from every part of NCI's funding: individual research grants, cancer center grants, large research teams, and training awards. Our tool can already answer a question like "what data did this cancer center's grant leave behind?" Starting in October 2026, NIH requires grant holders to report on their data sharing in their yearly progress reports. Our check gives program staff an independent way to see what was actually shared.

## Prompt 3: Innovation and Awareness of Existing Efforts

**What already exists.** We looked hard at what others have built. The pieces exist, but no one has put them together this way.

- **Tools that read attachments for computers.** The National Library of Medicine's FAIR-SMART system (2025) collects these attachments and sorts their tables so computer programs can search them. A Swiss team (2025) made 36 million attachments searchable by keyword. These are powerful, but they are built for machines and searches. They do not decide which files are real datasets, do not give them permanent links, and do not put them in NCI's catalogue. FAIR-SMART would make a good starting point for our work, not a replacement.
- **Some publishers already give files permanent links.** Two publishers, BMC and PLOS, automatically copy their attachments to a site called Figshare, which gives each one a permanent link. That covers about a fifth of the datasets we found. But those records carry the publisher's details, which can leave NCI uncredited, as with our brain tumor example, and none of them appear in NCI's catalogue. The other publishers, including Nature journals, which hold the largest share, do nothing like this.
- **Research on the problem.** Earlier studies showed that most papers point to attachments instead of proper repositories, and that permanent links last far longer than ordinary web links.
- **NCI's own catalogue.** The Index of NCI Studies already collects datasets from major data repositories and already uses automated tools to improve its records. But it collects nothing from paper attachments. Adding one more source is a natural next step for it, not a new system.

**What is new.** Other projects help computers search papers. Ours does three things none of them do.

1. **We measured NCI's own blind spot.** Not "data is hard to find" in general, but a count: NCI grants worth $11.2 billion produced papers holding 9,543 datasets, and 7,335 of them have no permanent link of their own. We could find no one who has counted this for any funder before. We also showed it is still happening today, and that every NIH institute we checked has the same problem.
2. **The work is already done, not just proposed.** We opened all 25,000 attachments. We proved the rescued data works by combining it into a 1,037-patient result. We built the file NCI's catalogue can load right now. And we put up a live tool where anyone, including a program officer, can type in a grant number and see what data it left behind.
3. **It is built for NCI.** Other systems serve search engines and programmers. Ours answers the questions NCI's own staff ask: what did our grants produce, where is it, and how do we get it into our own catalogue? And the fix costs almost nothing.

In short: others describe the problem. We measured it for NCI, prepared the fix for every paper, and are handing NCI the result.

**What we are not proposing.** We are not building a new repository or a new catalogue, and we are not replacing NIH's 2023 policy. Attachment Rescue fills in everything published before that policy, and catches what still slips through after it.

## Prompt 4: Transferability, Sustainability, and Feasibility

**How NCI could adopt it.** Every part already exists and is run by someone else. The papers and attachments are public. Free repositories give out permanent links. NCI's catalogue already accepts new data sources. Adopting Attachment Rescue means adding one new source to that catalogue. It is a decision, not a construction project.

**What it would cost.** Very little. Checking a paper takes seconds of computer time. People are needed mainly to spot-check the descriptions, and for one conversation with the catalogue team. The file they would load is already built.

**Honest limits and how we handle them.**

- **Permission to copy.** Most of these papers, about four in five, use open licenses that allow copying. For the rest, we link to the original instead of making a copy.
- **Respecting authors.** No one should upload other people's files without telling them. The best option is for NCI to act as the official uploader, the way NIH already handles its own staff's papers. Otherwise, authors get 60 days' notice and a simple way to say no. If they say no, we only link to their file. Either way, the original authors are always credited, and any table about patients gets an extra review before it is copied.
- **Not every table is equally useful.** Some rescued tables are analysis results rather than raw measurements. Each record says which kind it is, so users know what they are getting.
- **Avoiding duplicates.** Some of these files were also shared elsewhere, or already have a publisher's link. We check for that first and reuse the existing link instead of making a second one.
- **The one outside decision.** NCI's catalogue team would need to agree to add the new source. If they do not, the datasets still get permanent links in public repositories, and our count still stands.

**How it lasts.** After the backlog is done, the system checks new papers every three months and checks every link once a month. Both run automatically. The dataset file and our full count are public, so anyone can rerun or improve them.

## Use of Generative AI

We used generative AI (Anthropic's Claude) to help write and run our analysis code, to help draft and edit this narrative, and to draft the plain-English dataset descriptions. Every number comes from our scripts, which anyone can rerun using public data. A separate, earlier check of 90 decisions was done with the AI assistant; the blind check of 30 files was done by the submitter. Both are published so others can review them. All decisions about what to claim and recommend are the submitter's own, and the submitter takes full responsibility for the content.
