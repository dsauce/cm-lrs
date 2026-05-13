# W2 — Precedent Retrieval: Corpus (30 documents)

**Workflow:** LLM is given the entire corpus and a retrieval query (e.g. "find all change-of-control put provisions in this corpus"). The LLM must return:

- A list of matching documents.
- The specific clause or passage in each matching document.
- A short comparative synthesis.

Tests evidence traceability (does it cite source?), factual accuracy (does the cited passage actually say that?), workflow completeness (did it find all matches?), source discipline (did it avoid claims unsupported by the corpus?).

**Corpus composition.** 30 documents:

- **22 EDGAR 424B5 senior-notes prospectuses** filed 2024–2025 across sectors.
- **5 documents reused from W1** (already in `corpus/W1_debt_terms/edgar_picks.md`) — included so the same paper exhibits can cite consistent source material.
- **3 synthetic Nordic-style term sheets** from W1 (located in `corpus/W1_debt_terms/synthetic/`) — added to inject covenant structures (LTV, ICR, green-bond framework, Nordic-style change-of-control language) that don't always appear in US IG prospectuses, ensuring the retrieval queries exercise full breadth.

All 27 EDGAR documents share the same URL pattern: `https://www.sec.gov/Archives/edgar/data/{CIK}/{accession-no-dashes}/{primary-doc}`.

---

## Group A — Reused from W1 (5 docs)

| # | Issuer | CIK | Accession | Sector | Note |
|---|---|---|---|---|---|
| 1 | HCA Inc. | 0000860730 | 0001193125-24-197839 | Healthcare provider | Multi-tranche, complex parent/sub guarantees |
| 2 | Netflix, Inc. | 0001065280 | 0001140361-24-035134 | Media / streaming | Single-issuer baseline |
| 3 | Dell International L.L.C. / EMC Corp | 0001476297 / 0000790070 | 0001193125-24-232279 | Tech | Co-issuer structure |
| 4 | Broadcom Inc. | 0001730168 | 0001193125-24-226546 | Tech | Post-VMware acquisition financing |
| 5 | Cencora, Inc. | 0001140859 | 0001104659-24-124327 | Healthcare distribution | Renamed issuer (formerly AmerisourceBergen) |

URLs and verification details: see `corpus/W1_debt_terms/edgar_picks.md`.

---

## Group B — Additional EDGAR 424B5 prospectuses (22 docs)

All filed 2024–2025; verified accessible via EDGAR full-text search. Filing index URL: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=424B5`. Specific document filenames within each accession to be confirmed at evaluation-time fetch.

| # | Issuer | CIK | Accession | Filed | Sector |
|---|---|---|---|---|---|
| 6 | CDW Corp | 0001402057 | 0001193125-24-200631 | 2024-08-14 | Tech distribution |
| 7 | Starbucks Corp | 0000829224 | 0001213900-25-040692 | 2025-05-07 | Consumer / coffee |
| 8 | BorgWarner Inc. | 0000908255 | 0001104659-24-087671 | 2024-08-09 | Automotive supplier |
| 9 | Toll Brothers, Inc. | 0000794170 | 0001628280-25-030013 | 2025-06-06 | Homebuilder |
| 10 | D.R. Horton, Inc. | 0000882184 | 0001193125-25-098542 | 2025-04-28 | Homebuilder |
| 11 | Las Vegas Sands Corp | 0001300514 | 0001300514-25-000098 | 2025-04-29 | Gaming / hospitality |
| 12 | Tapestry, Inc. | 0001116132 | 0001140361-24-048675 | 2024-12-03 | Consumer / luxury (initial 048248 was withdrawn; corrected 2026-05-12) |
| 13 | Amphenol Corp | 0000820313 | 0001104659-24-112292 | 2024-10-29 | Electronics |
| 14 | Agilent Technologies, Inc. | 0001090872 | 0001193125-24-212662 | 2024-09-04 | Life sciences instruments |
| 15 | Take-Two Interactive Software Inc | 0000946581 | 0001193125-24-157939 | 2024-06-10 | Gaming software |
| 16 | Cintas Corporation No. 2 | 0001182641 | 0001193125-25-103869 | 2025-04-29 | Industrial services |
| 17 | Crown Castle Inc. | 0001051470 | 0001193125-24-190758 | 2024-08-01 | Telecom infrastructure REIT |
| 18 | Fiserv Inc. | 0000798354 | 0001193125-25-107149 | 2025-04-30 | Financial services |
| 19 | Sysco Corp | 0000096021 | 0001193125-25-025670 | 2025-02-13 | Food distribution |
| 20 | Westinghouse Air Brake Tech (Wabtec) | 0000943452 | 0001140361-25-019669 | 2025-05-19 | Rail equipment |
| 21 | Labcorp Holdings Inc. | 0000920148 | 0001193125-24-219238 | 2024-09-16 | Diagnostics |
| 22 | Expedia Group, Inc. | 0001324424 | 0001140361-25-005072 | 2025-02-19 | Travel marketplace |
| 23 | Micron Technology Inc. | 0000723125 | 0001104659-25-039497 | 2025-04-25 | Semiconductors |
| 24 | Waste Management Inc. | 0000823768 | 0001104659-24-113068 | 2024-10-31 | Environmental services |
| 25 | Georgia Power Co | 0000041091 | 0000041091-24-000008 | 2024-02-20 | Regulated utility |
| 26 | Southern Co | 0000092122 | 0000092122-24-000079 | 2024-09-04 | Utility holding company |
| 27 | Southern Co Gas | 0001004155 | 0001004155-24-000002 | 2024-09-03 | Regulated gas utility |

### Sector coverage check

Across Groups A and B, the 27 EDGAR prospectuses span: **healthcare (3) · tech (5) · media/gaming (3) · consumer (3) · homebuilding (2) · industrials (3) · financial services (1) · transport/travel (3) · utilities (3) · REIT (1)**. No single sector dominates; this prevents the retrieval task from collapsing into a single-sector retrieval problem.

---

## Group C — Synthetic Nordic term sheets (3 docs)

| # | Title | File | Style mirrored |
|---|---|---|---|
| 28 | Nordhavn Industri AB | `corpus/W1_debt_terms/synthetic/ts_01_nordhavn_industri.md` | Swedish-law senior secured FRN, industrials |
| 29 | Fjordkraft Energi Holding AS | `corpus/W1_debt_terms/synthetic/ts_02_fjordkraft_energi.md` | Norwegian-law senior unsecured green FRN |
| 30 | Karelis Real Estate ApS | `corpus/W1_debt_terms/synthetic/ts_03_karelis_real_estate.md` | Danish-law senior secured FRN, real estate, LTV/ICR covenants |

These three add covenant structures that are atypical in US IG prospectuses — floating EURIBOR/STIBOR pricing, LTV-based incurrence tests, green-bond reporting obligations, sustainability-linked redemption — ensuring the retrieval queries do not trivially over-fit to US conventions.

---

## Open follow-ups

1. **Document type diversification.** Currently 27 of 30 documents are 424B5 prospectus supplements. A future revision may swap 5 for indenture exhibits (Exhibit 4.1 to 8-K) which have denser covenant text than the equity-marketing-oriented prospectus supplement. Decide at scoring time whether to swap.
2. **Nordic regulator content.** None included yet. If Prerit wants to test the LLM's handling of Swedish-language extracts (Finansinspektionen prospectuses are bilingual in places), add 2–3 SE/NO regulator filings as a follow-up corpus extension. The redistribution position needs to be checked first.
3. **Document fetching at evaluation time.** Within each accession, the specific primary-doc filename is regular but not standardised. A small script will resolve `https://www.sec.gov/Archives/edgar/data/{CIK}/{accession-no-dashes}/` and pull the largest 424B5 .htm — that pattern was verified on the W1 picks.

---

*Compiled 2026-05-12.*
