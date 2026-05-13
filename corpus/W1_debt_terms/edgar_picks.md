# W1 — Debt-Terms Extraction: EDGAR Prospectus Picks

**Workflow:** LLM extracts and normalises lender / covenant / pricing terms from a bond prospectus into a structured table. Tests factual accuracy, numerical consistency, evidence traceability.

**Corpus size after expansion (2026-05-12 v2):** 15 real EDGAR prospectuses + 3 synthetic Nordic HY term sheets = 18 documents.

**Selection criteria:**
- All public on SEC EDGAR — free, redistributable.
- Mix of sectors (no single-sector clustering).
- Mix of structural complexity (single-issuer → multi-entity co-issuers; senior unsecured → first-mortgage bonds).
- All filed 2024–2025 to keep terms recent.
- All 424B5 (prospectus supplements under shelf registration) — these are the actual takedown documents with full commercial terms.

**Sector coverage across the 15 real prospectuses:** healthcare provider · healthcare distribution · streaming media · tech (3, incl. co-issuer) · consumer / coffee · automotive supplier · gaming & hospitality · life-sciences instruments · telecom REIT · financial services · travel marketplace · semiconductors · regulated utility · environmental services.

---

## Pick 1 — HCA Inc. (Healthcare provider)

| Field | Value |
|---|---|
| Issuer | HCA Inc. (wholly-owned subsidiary of HCA Healthcare, Inc.) |
| CIK | 0000860730 |
| Filed | 2024-08-09 |
| Form | 424B5 |
| Accession | 0001193125-24-197839 |
| Offering | US$3.0bn senior notes in 3 tranches: 5.450% due 2031, 5.450% due 2034, 5.950% due 2054 |
| Document URL | https://www.sec.gov/Archives/edgar/data/860730/000119312524197839/d873032d424b5.htm |
| File size | ~709 KB |
| Verified | 2026-05-12 — HTTP 200, cover page inspected |

**Why this one:** large multi-tranche senior notes deal from an HY-cusp issuer; complex parent/sub guarantee structure with HCA Inc. as issuer and HCA Healthcare as parent; rich covenant package typical of leveraged healthcare.

---

## Pick 2 — Netflix, Inc. (Media / streaming)

| Field | Value |
|---|---|
| Issuer | Netflix, Inc. |
| CIK | 0001065280 |
| Filed | 2024-07-31 |
| Form | 424B5 |
| Accession | 0001140361-24-035134 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1065280/000114036124035134/ny20032950x4_424b5.htm |
| File size | ~711 KB |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** single-issuer structure as a baseline; well-known IG streaming-media issuer; demonstrates LLM can handle a "clean" prospectus without confusing parent/sub language.

---

## Pick 3 — Dell International L.L.C. / EMC Corporation (Tech, co-issuers)

| Field | Value |
|---|---|
| Issuers | Dell International L.L.C. and EMC Corporation (co-issuers) |
| Parent | Dell Inc. (filing CIK) |
| CIK | 0000790070 (parent) / 0001476297 (Dell Intl) |
| Filed | 2024-10-03 |
| Form | 424B5 |
| Accession | 0001193125-24-232279 |
| Offering | US$1.5bn senior notes in 2 tranches: 4.350% due 2030, 4.850% due 2035 |
| Document URL | https://www.sec.gov/Archives/edgar/data/790070/000119312524232279/d866647d424b5.htm |
| File size | ~538 KB |
| Verified | 2026-05-12 — HTTP 200, cover page inspected |

**Why this one:** co-issuer structure is a common LLM stumbling block. Post-LBO legacy capital structure provides covenant texture not present in pure IG issuers.

---

## Pick 4 — Broadcom Inc. (Tech, post-acquisition)

| Field | Value |
|---|---|
| Issuer | Broadcom Inc. |
| CIK | 0001730168 |
| Filed | 2024-09-26 (preliminary supplement) |
| Form | 424B5 |
| Accession | 0001193125-24-226546 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1730168/000119312524226546/d860719d424b5.htm |
| File size | ~583 KB |
| Verified | 2026-05-12 — HTTP 200 |
| Note | Preliminary supplement; swap to final 424B5 if preferred |

**Why this one:** Broadcom's post-VMware acquisition refinancing context gives interesting use-of-proceeds and risk-factor language; large IG issuer with complex global subsidiary footprint.

---

## Pick 5 — Cencora, Inc. (Healthcare distribution)

| Field | Value |
|---|---|
| Issuer | Cencora, Inc. (formerly AmerisourceBergen) |
| CIK | 0001140859 |
| Filed | 2024-12-02 (preliminary supplement) |
| Form | 424B5 |
| Accession | 0001104659-24-124327 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1140859/000110465924124327/tm2429220-3_424b5.htm |
| File size | ~850 KB |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** renamed-issuer scenario tests LLM handling of historical references to "AmerisourceBergen" — a soft trap for hallucination.

---

## Pick 6 — Starbucks Corporation (Consumer / coffee)

| Field | Value |
|---|---|
| Issuer | Starbucks Corporation |
| CIK | 0000829224 |
| Filed | 2025-05-07 |
| Form | 424B5 |
| Accession | 0001213900-25-040692 |
| Document URL | https://www.sec.gov/Archives/edgar/data/829224/000121390025040692/ea0240971-02.htm |
| File size | ~969 KB |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** consumer-discretionary IG benchmark with global supply-chain exposure; clean single-issuer senior unsecured structure; useful for testing baseline extraction against a household-name issuer.

---

## Pick 7 — BorgWarner Inc. (Automotive supplier)

| Field | Value |
|---|---|
| Issuer | BorgWarner Inc. |
| CIK | 0000908255 |
| Filed | 2024-08-09 |
| Form | 424B5 |
| Accession | 0001104659-24-087671 |
| Document URL | https://www.sec.gov/Archives/edgar/data/908255/000110465924087671/tm2415069-5_424b5.htm |
| File size | ~779 KB |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** automotive-supplier IG name with EV-transition risk-factor language; tests handling of cyclical-industry risk disclosure and capital-allocation discussion.

---

## Pick 8 — Las Vegas Sands Corp (Gaming & hospitality)

| Field | Value |
|---|---|
| Issuer | Las Vegas Sands Corp |
| CIK | 0001300514 |
| Filed | 2025-04-29 |
| Form | 424B5 |
| Accession | 0001300514-25-000098 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1300514/000130051425000098/lasvegassandscorp424b5prel.htm |
| File size | ~2.0 MB |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** consumer-cyclical with Macau / Singapore geographic concentration; concession-renewal risk factors; largest file in the W1 set (2 MB) tests LLM context-handling.

---

## Pick 9 — Agilent Technologies, Inc. (Life-sciences instruments)

| Field | Value |
|---|---|
| Issuer | Agilent Technologies, Inc. |
| CIK | 0001090872 |
| Filed | 2024-09-04 |
| Form | 424B5 |
| Accession | 0001193125-24-212662 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1090872/000119312524212662/d886539d424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** life-sciences-instrument issuer (distinct from healthcare provider / distribution); useful as an edge case in W2's healthcare-sector classification query.

---

## Pick 10 — Crown Castle Inc. (Telecom infrastructure REIT)

| Field | Value |
|---|---|
| Issuer | Crown Castle Inc. |
| CIK | 0001051470 |
| Filed | 2024-08-01 |
| Form | 424B5 |
| Accession | 0001193125-24-190758 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1051470/000119312524190758/d814781d424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** REIT structure introduces FFO/AFFO disclosure and REIT-specific covenant language (asset-disposal proceeds tied to qualifying real-estate test). Cross-references W2 Q3 (REIT classification).

---

## Pick 11 — Fiserv Inc. (Financial services)

| Field | Value |
|---|---|
| Issuer | Fiserv, Inc. |
| CIK | 0000798354 |
| Filed | 2025-04-30 |
| Form | 424B5 |
| Accession | 0001193125-25-107149 |
| Document URL | https://www.sec.gov/Archives/edgar/data/798354/000119312525107149/d768118d424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** payments-processor IG name; financial-services sector adds diversity vs. industrial / consumer / healthcare bias; tests LLM extraction on sector-specific risk language.

---

## Pick 12 — Expedia Group, Inc. (Travel marketplace)

| Field | Value |
|---|---|
| Issuer | Expedia Group, Inc. |
| CIK | 0001324424 |
| Filed | 2025-02-19 |
| Form | 424B5 |
| Accession | 0001140361-25-005072 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1324424/000114036125005072/ny20042512x2_424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** travel-marketplace issuer with multiple consumer brands; recovery-cycle narrative; risk-factor disclosure spans cyclical, geopolitical and consumer-spending exposures.

---

## Pick 13 — Micron Technology Inc. (Semiconductors)

| Field | Value |
|---|---|
| Issuer | Micron Technology, Inc. |
| CIK | 0000723125 |
| Filed | 2025-04-25 |
| Form | 424B5 |
| Accession | 0001104659-25-039497 |
| Document URL | https://www.sec.gov/Archives/edgar/data/723125/000110465925039497/tm2511594-4_424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** memory-semiconductor cyclical issuer; cycle-stage risk disclosure; export-control geopolitical risk factors typical of recent semi prospectuses.

---

## Pick 14 — Georgia Power Company (Regulated utility — first mortgage bonds)

| Field | Value |
|---|---|
| Issuer | Georgia Power Company |
| CIK | 0000041091 |
| Filed | 2024-02-20 |
| Form | 424B5 |
| Accession | 0000041091-24-000008 |
| Document URL | https://www.sec.gov/Archives/edgar/data/41091/000004109124000008/gpc2024bsnpreprosup.htm |
| Verified | 2026-05-12 — HTTP 200, cover page inspected |

**Why this one:** regulated-utility issuer with **first mortgage bond** structure — a fundamentally different security and covenant style from senior unsecured notes. Tests LLM ability to recognise and extract structural differences (mortgaged property, release-and-substitution covenants, additional-bond test) rather than forcing them into a generic senior-notes template.

---

## Pick 15 — Waste Management, Inc. (Environmental services)

| Field | Value |
|---|---|
| Issuer | Waste Management, Inc. |
| CIK | 0000823768 |
| Filed | 2024-10-31 |
| Form | 424B5 |
| Accession | 0001104659-24-113068 |
| Document URL | https://www.sec.gov/Archives/edgar/data/823768/000110465924113068/tm2426919-4_424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** environmental-services IG name with infrastructure-style cash flows; recent post-acquisition financing context (Stericycle); tests handling of acquisition-financing use-of-proceeds language.

---

## Synthetic supplement (3 documents)

In addition to the 15 real prospectuses above, three synthetic Nordic HY term sheets are kept in `corpus/W1_debt_terms/synthetic/`:

| File | Style mirrored | Why kept |
|---|---|---|
| `ts_01_nordhavn_industri.md` | Swedish-law senior secured FRN, industrials | I authored these — byte-perfect ground truth for scoring. The "right answer" for extraction is known exactly, eliminating my own reading-error risk from the rubric. |
| `ts_02_fjordkraft_energi.md` | Norwegian-law senior unsecured green FRN, renewables | Same. |
| `ts_03_karelis_real_estate.md` | Danish-law senior secured FRN, LTV/ICR covenants | Same. |

The synthetics are explicitly flagged as fictional in their headers; they are not used in the paper as real-deal evidence.

---

## Open follow-ups

1. Picks 4 (Broadcom) and 5 (Cencora) are preliminary supplements. The final 424B5 supplements (filed 1–2 days later) are commercially identical but say "subject to completion" was removed. Swap if preferred.
2. None of the 15 are true HY (most large HY issuers issue under Rule 144A which doesn't appear on EDGAR). For a HY-heavy variant, the cleanest substitutions would be registered exchange offers (e.g., Carnival, Tenet, CCO Holdings), which can be added later if Prerit wants the HY angle strengthened.
3. None of the 15 are Nordic-domiciled. The Nordic angle is carried by the 3 synthetics, by Spotify in W3, and by the option to add Finansinspektionen / Finanstilsynet filings if the redistribution position is resolved.

---

*Compiled 2026-05-12 (v1: 5 picks). Expanded 2026-05-12 (v2: 15 picks). URLs verified by curl with deterministic EDGAR pattern.*
