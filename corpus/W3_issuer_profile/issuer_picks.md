# W3 — Issuer Profile: Issuer Picks

**Workflow:** LLM synthesises a coherent profile of an issuer from public filings — business model, segments, risk factors, financial trajectory, capital structure — with evidence trails to specific source passages. Tests workflow completeness, source discipline, decision usefulness.

**Corpus size after expansion (2026-05-12 v2):** 5 issuers × 3 documents = 15 documents.

**Selection rationale.** A first pass considered Nordic-listed issuers (Volvo Cars, Vestas, Telia). Their IR pages are JavaScript-rendered, making canonical PDF URLs unstable to cite in a paper. To keep the corpus uniformly retrievable, the five picks below are all SEC-registered with EDGAR-stable URLs. Sector diversity covers: EV / automotive · luxury auto · digital-infrastructure REIT · audio streaming · financial exchanges. Spotify retains the Nordic angle (Stockholm HQ, NYSE-listed). Three filing-format variants are present (10-K, 20-F, 10-K), so the LLM cannot collapse to a single annual-filing template.

| Field | Pick 1 — Tesla | Pick 2 — Equinix | Pick 3 — Spotify | Pick 4 — Ferrari | Pick 5 — CME Group |
|---|---|---|---|---|---|
| Sector | EV / energy / AI | Digital infrastructure (REIT) | Audio streaming | Luxury automotive | Financial exchanges |
| Geography | US-domiciled | US-domiciled | Stockholm HQ, Luxembourg-domiciled | Maranello HQ, Netherlands-domiciled | US-domiciled |
| Filing status | US domestic registrant | US domestic registrant | Foreign Private Issuer | Foreign Private Issuer | US domestic registrant |
| Annual filing format | 10-K | 10-K | 20-F | 20-F | 10-K |

---

## Pick 1 — Tesla, Inc.

| Field | Value |
|---|---|
| CIK | 0001318605 |
| Ticker | TSLA (Nasdaq) |
| Latest annual filing | 10-K for FY2025, filed Q1 2026 |
| Accession | 0001628280-26-003952 |
| Document URL — 10-K | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm |
| Filing index | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/ |
| Latest quarterly | 10-Q, accession 0001628280-26-026673 |
| Quarterly index | https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/ |
| Investor presentation | Filed quarterly as 8-K Exhibit 99 around earnings releases — to be pulled fresh at evaluation time from the EDGAR 8-K filings list |
| Verified | 2026-05-12 — URLs resolve |

**Why this one:** complex multi-segment issuer (automotive, energy generation & storage, services, AI/robotics); rich and contested risk-factor disclosure; capital structure spans common stock, convertible notes, and ABS programmes. Strong stress test for the LLM's ability to maintain factual discipline against background noise.

---

## Pick 2 — Equinix, Inc.

| Field | Value |
|---|---|
| CIK | 0001101239 |
| Ticker | EQIX (Nasdaq) |
| Latest annual filing | 10-K for FY2025, filed Q1 2026 |
| Accession | 0001101239-26-000032 |
| Document URL — 10-K | https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/eqix-20251231.htm |
| Filing index | https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/ |
| Latest quarterly | 10-Q, accession 0001628280-25-021086 |
| Quarterly index | https://www.sec.gov/Archives/edgar/data/1101239/000162828025021086/ |
| Investor presentation | Quarterly earnings call deck as 8-K Exhibit 99 — pull fresh at evaluation time |
| Verified | 2026-05-12 — URLs resolve |

**Why this one:** REIT structure introduces specialised disclosure (FFO, AFFO, capacity utilisation, MRR/ARR style operating metrics) that ordinary corporate-LLM training has thinner coverage on. Global colocation/data-centre business with extensive geographic segmentation. Tests whether the LLM correctly handles real-estate-style metrics without forcing them into a generic SaaS or industrial-corporate template.

---

## Pick 3 — Spotify Technology S.A.

| Field | Value |
|---|---|
| CIK | 0001639920 |
| Ticker | SPOT (NYSE) |
| Filing status | Foreign Private Issuer (Luxembourg-domiciled, NYSE-listed, files 20-F annually + 6-K reports) |
| Latest annual filing | 20-F for FY2025, filed 2026 |
| Accession | 0001628280-26-006874 |
| Document URL — 20-F | https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm |
| Filing index | https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ |
| Latest interim filing | 6-K, accession 0001628280-26-027951 |
| Interim index | https://www.sec.gov/Archives/edgar/data/1639920/000162828026027951/ |
| Verified | 2026-05-12 — URLs resolve |

**Why this one:** 20-F format differs structurally from 10-K (more narrative, more international risk disclosure, different segment conventions). Two-tier capital structure (Class A and beneficiary certificates). MAU / Premium Subscribers as primary operating metric. Tests LLM ability to identify the correct annual filing format for a foreign private issuer rather than defaulting to 10-K conventions.

Also: Stockholm-headquartered, preserving the Nordic angle dropped when European-listed candidates were ruled out for URL stability.

---

## Pick 4 — Ferrari N.V. (Luxury automotive)

| Field | Value |
|---|---|
| CIK | 0001648416 |
| Ticker | RACE (NYSE) |
| Filing status | Foreign Private Issuer (Netherlands-domiciled, NYSE-listed, files 20-F + 6-K) |
| Latest annual filing | 20-F for FY2025, filed Q1 2026 |
| Accession | 0001648416-26-000024 |
| Document URL — 20-F | https://www.sec.gov/Archives/edgar/data/1648416/000164841626000024/race-20251231.htm |
| Filing index | https://www.sec.gov/Archives/edgar/data/1648416/000164841626000024/ |
| Latest interim filing | 6-K, accession 0001648416-26-000066 |
| Interim index | https://www.sec.gov/Archives/edgar/data/1648416/000164841626000066/ |
| Verified | 2026-05-12 — URLs resolve |

**Why this one:** luxury-automotive narrative is sharply different from Tesla's EV / mass-market framing — tests LLM ability to distinguish two automotive issuers without collapsing them into a single "auto" template. Italian operating heritage with Dutch domicile creates jurisdiction-mix in risk disclosure. Limited-volume / waitlist-driven order book is a unique operating metric.

---

## Pick 5 — CME Group Inc. (Financial exchanges)

| Field | Value |
|---|---|
| CIK | 0001156375 |
| Ticker | CME (Nasdaq) |
| Latest annual filing | 10-K for FY2025, filed Q1 2026 |
| Accession | 0001156375-26-000009 |
| Document URL — 10-K | https://www.sec.gov/Archives/edgar/data/1156375/000115637526000009/cme-20251231.htm |
| Filing index | https://www.sec.gov/Archives/edgar/data/1156375/000115637526000009/ |
| Latest quarterly | 10-Q, accession 0001156375-26-000020 |
| Quarterly index | https://www.sec.gov/Archives/edgar/data/1156375/000115637526000020/ |
| Verified | 2026-05-12 — URLs resolve |

**Why this one:** financial-exchange business with regulatory-revenue exposure (notional trading volume drives revenue per asset class — equities / interest rates / FX / energy / agricultural commodities / metals). Specialised market-structure risk factors. As an exchange operator it sits within capital markets — directly relevant to the paper's framing without being an investment-banking employer-sensitive name.

---

## Documents per issuer (target for evaluation)

For each issuer, the workflow inputs are:

1. **Annual report** (10-K or 20-F) — verified URL above.
2. **Most recent quarterly** (10-Q or 6-K) — index URL above; primary document name can be derived at evaluation time.
3. **Most recent earnings investor presentation** — filed as 8-K Exhibit 99 (US registrants) or 6-K (Spotify, Ferrari). These are best pulled fresh at evaluation time from the EDGAR filings list filtered to the relevant accession date; the URLs change every quarter and listing them statically here would invite link rot.

Total documents at evaluation time: **15** (5 issuers × 3 documents).

---

## Open follow-ups

1. Confirm with Prerit whether the SEC-issuer pivot is acceptable, or whether to invest more effort retrieving Nordic IR PDFs (would likely require Playwright or a manual URL share from Prerit).
2. At evaluation time, capture the specific 8-K / 6-K accession for the most recent earnings deck.

---

*Compiled 2026-05-12. URLs verified by curl HEAD + filing-index inspection.*
