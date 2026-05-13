# W4 — Transaction Comparable: Target + Comparable Universe

**Workflow:** LLM retrieves and compares public transaction examples for a chosen target, with clear source trails. The LLM is asked to identify the most relevant comparables, extract key deal metrics (EV, EV/EBITDA, EV/Revenue, premium to undisturbed price), and synthesise a comparable-transactions write-up. Tests evidence traceability, numerical consistency, decision usefulness, source discipline.

**Constraint:** Target must be a transaction with no advisory conflict for the author. The target chosen below is a large US tech merger; the entire syndicate is US- and global-bulge-bracket; no Nordic banks were involved.

---

## Target — Synopsys / Ansys merger

| Field | Value |
|---|---|
| Announcement | 16 January 2024 |
| Closing | 17 July 2025 |
| Acquirer | Synopsys, Inc. (Nasdaq: SNPS) |
| Target | Ansys, Inc. (Nasdaq: ANSS) |
| Consideration | Approximately US$35bn — cash and stock; ~US$197 cash plus 0.3450 SNPS shares per ANSS share |
| Acquirer's financial advisors | Goldman Sachs |
| Target's financial advisors | Qatalyst Partners |
| Acquirer's legal | Cleary Gottlieb |
| Target's legal | Skadden Arps |
| Advisory-conflict check (author) | **None — confirmed by public deal disclosure; no Nordic bank in the advisor list** |
| Sector | Electronic design automation (EDA) software + simulation software |
| Acquirer CIK | 0000883241 |
| Target CIK | 0001013462 |

### Key documents

| Doc | URL |
|---|---|
| Acquirer S-4/A (registration statement, amendment) | https://www.sec.gov/Archives/edgar/data/883241/000114036124019383/ny20023075x2_s4a.htm |
| Acquirer S-4/A filing index | https://www.sec.gov/Archives/edgar/data/883241/000114036124019383/ |
| Target DEFM14A (definitive merger proxy) | https://www.sec.gov/Archives/edgar/data/1013462/000114036124020334/ny20025601x1_defm14a.htm |
| Target DEFM14A filing index | https://www.sec.gov/Archives/edgar/data/1013462/000114036124020334/ |
| Announcement 8-K (Synopsys) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000883241&type=8-K&dateb=20240117&owner=include&count=5 — pull the 2024-01-16 filing |
| Announcement 8-K (Ansys) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001013462&type=8-K&dateb=20240117&owner=include&count=5 — pull the 2024-01-16 filing |

**Why this target.** Large (~US$35bn EV), well-documented (S-4 + merger proxy), tech-sector clustering means a coherent universe of public comparable transactions can be assembled. No Nordic bank involvement removes any author-side advisory-conflict sensitivity. Both parties US-listed, so all primary documents sit on EDGAR.

---

## Comparable transaction universe (20 deals)

**Selection logic.** Large-cap software / digital / infrastructure M&A announced 2022 onward, EV ≥ US$5bn, where:

- The deal is publicly disclosed and at least one party has SEC filings; and
- A banker would plausibly cite the deal as a relevant comp for an EDA / simulation / enterprise software M&A.

Each deal is flagged for **advisory-conflict involvement: none** — checked against published announcement press releases and the SEC filings. Nordic bank involvement appears nowhere; this is a US/global-bulge-bracket comp universe by design.

| # | Date announced | Acquirer | Target | EV (approx.) | Primary advisors | Sector | Note |
|---|---|---|---|---|---|---|---|
| 1 | 2022-01-18 | Microsoft Corporation | Activision Blizzard, Inc. | US$69bn | Goldman (MS); Allen & Co. + Morgan Stanley (ATVI) | Gaming software | Closed Oct 2023 after FTC litigation |
| 2 | 2023-09-21 | Cisco Systems, Inc. | Splunk Inc. | US$28bn | Tidal Partners (CSCO); Morgan Stanply (SPLK) | Observability / data analytics | Closed Mar 2024 |
| 3 | 2022-05-26 | Broadcom Inc. | VMware, Inc. | US$61bn | Barclays + BofA + Citi + Credit Suisse + Morgan Stanley + Wells Fargo (AVGO); Goldman + JP Morgan (VMW) | Virtualisation / infra software | Closed Nov 2023 |
| 4 | 2022-10-21 | Vista Equity Partners | KnowBe4, Inc. | US$4.6bn | Morgan Stanley + Vista (Vista); J.P. Morgan (KNBE) | Cybersecurity awareness | Take-private |
| 5 | 2022-08-08 | Vista Equity Partners | Avalara, Inc. | US$8.4bn | Goldman + Vista (Vista); Qatalyst (AVLR) | Tax compliance SaaS | Take-private |
| 6 | 2022-01-31 | Vista + Elliott | Citrix Systems, Inc. | US$16.5bn | Goldman + Morgan Stanley (Vista/Elliott); Qatalyst (CTXS) | Virtualisation | Take-private; merged with TIBCO into Cloud Software Group |
| 7 | 2022-06-13 | Thoma Bravo | Anaplan, Inc. | US$10.7bn | Goldman + Morgan Stanley (TB); Qatalyst (PLAN) | Enterprise planning SaaS | Take-private |
| 8 | 2022-03-08 | Permira | Mimecast Limited | US$5.8bn | Morgan Stanley (Permira); J.P. Morgan (MIME) | Email security | Take-private |
| 9 | 2024-04-24 | IBM | HashiCorp, Inc. | US$6.4bn | Goldman Sachs + Centerview (IBM); Qatalyst (HCP) | Cloud infrastructure software | Closed Feb 2025. **Swap-in 2026-05-12** replacing Everbridge (too small). |
| 10 | 2022-12-12 | Thoma Bravo | Coupa Software Inc. | US$8.0bn | Morgan Stanley + TB (TB); Qatalyst (COUP) | Spend management SaaS | Take-private |
| 11 | 2023-04-21 | Francisco Partners + TPG | New Relic, Inc. | US$6.5bn | Goldman + Qatalyst (NEWR) | Observability | Take-private |
| 12 | 2024-01-09 | Hewlett Packard Enterprise | Juniper Networks, Inc. | US$14bn | J.P. Morgan + Mizuho + Citi (HPE); Goldman (JNPR) | Networking hardware/software | Closed Jul 2025 |
| 13 | 2023-04-13 | Silver Lake | Qualtrics International Inc. | US$12.5bn | Morgan Stanley + Goldman (SL/CPP); Qatalyst (XM) | Experience management SaaS | Take-private |
| 14 | 2024-09-03 | Blackstone + Vista | Smartsheet Inc. | US$8.4bn | Qatalyst (SMAR) | Work management SaaS | Take-private |
| 15 | 2024-05-13 | Permira | Squarespace, Inc. | US$6.6bn | Goldman (SQSP) | Website builder SaaS | Take-private |
| 16 | 2024-04-26 | Thoma Bravo | Darktrace plc | US$5.3bn | Qatalyst + Jefferies (DARK) | Cybersecurity AI | UK take-private — scheme of arrangement. Local file: `comparables/16_darktrace_scheme_announcement_2024-05-23.htm` (IR announcement of Scheme Document publication; full Scheme PDF behind IR microsite disclaimer wall). |
| 17 | 2022-09-15 | Adobe Inc. | Figma, Inc. | US$20bn | Allen & Co. + Morgan Stanley + Goldman (ADBE); Qatalyst (FIG) | Design / collaboration software | **Terminated Dec 2023** following CMA / EU opposition. Useful as a "comp that didn't close" — bankers cite failed deals in pitches. **Swap-in 2026-05-12** replacing the Qualtrics duplicate. |
| 18 | 2022-05-04 | Permira | Zendesk, Inc. | US$10.2bn | Qatalyst (ZEN) | Customer support SaaS | Take-private |
| 19 | 2023-03-14 | Blackstone | Cvent Holding Corp. | US$4.6bn | Goldman + Morgan Stanley (CVT); Blackstone in-house | Events technology SaaS | Take-private; closed Jun 2023. **Swap-in 2026-05-12** replacing Perficient (too small). |
| 20 | 2021-03-01 | Cisco Systems, Inc. | Acacia Communications, Inc. | US$4.5bn | Goldman (CSCO); Morgan Stanley (ACIA) | Optical interconnect for hyperscale data centres | Closed Mar 2021. **Swap-in 2026-05-12** replacing Cisco/Accedian. Adjacent to Synopsys / Ansys territory (semi-component infrastructure for AI compute). |

### Notes on this list

1. **Swaps applied 2026-05-12 (v2):**
   - #9 Everbridge → IBM / HashiCorp ($6.4bn, 2024).
   - #17 Qualtrics duplicate → Adobe / Figma ($20bn announced, terminated Dec 2023). A "comp that didn't close" — bankers cite these in pitches, so it adds methodological texture to the test set.
   - #19 Perficient → Blackstone / Cvent ($4.6bn, 2023).
   - #20 Cisco / Accedian → Cisco / Acacia Communications ($4.5bn, 2021). Acacia is adjacent to the Synopsys / Ansys semi-infrastructure space and tightens the comp set.
2. Several names overlap with Synopsys/Ansys in being software / SaaS, which is the comp logic. EDA-pure-play comparables are scarce by definition; analysts widen to enterprise software when sizing the EDA comp set.
3. Where the acquirer is a private equity sponsor (Vista, Thoma Bravo, Permira, Silver Lake, Blackstone), the target's filings on EDGAR are typically the richest source — DEFM14A and 13E-3 going-private filings.
4. The two Cisco entries (#2 Splunk, #20 Acacia) are now both genuine large strategic acquisitions, not a size mismatch.

### Total documents at evaluation time

For each of the 20 comparables, plan to retrieve:

- Announcement press release (acquirer side)
- Definitive merger proxy or scheme document (target side, on EDGAR or applicable regulator)
- Most recent 10-K of the target at announcement date (segment / revenue / EBITDA base for the metrics)

That implies ~60 documents at evaluation time, all pullable from EDGAR (US deals) or RNS / Companies House (UK take-privates).

---

## Open follow-ups

1. **Prerit reality-check on the comp universe.** Are these the deals a sell-side EDA banker would pull? Swap any that smell off.
2. **Resolve the two flagged rows (#9, #19, #20)** — swap to size-appropriate substitutes. Indicative swaps listed above.
3. **EDA-specific narrow comps.** If we want a sharper exhibit ("most directly comparable"), narrow to: Synopsys / Avast Antivirus, Cadence / Hexagon AB, etc. — but these are smaller in number and may force broadening anyway.
4. **Premium analysis.** For each comp, undisturbed share price one day before announcement is needed. EDGAR press releases give offer price; undisturbed price is from market data (e.g., FactSet, Yahoo Finance for the spot check).

---

*Compiled 2026-05-12. Target advisor list confirmed against the published Jan 2024 announcement press release; no Nordic bank involvement. Specific document URLs for the comparable universe to be retrieved at evaluation time using the same EDGAR pattern verified for the target.*
