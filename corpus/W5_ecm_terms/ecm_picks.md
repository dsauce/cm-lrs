# W5 — ECM Transaction Terms Extraction: Document Picks

**Workflow:** LLM extracts and normalises ECM transaction terms from a single prospectus into a structured table. Mirrors W1's shape (debt-terms extraction) on the equity side.

**Total documents:** 10 real EDGAR prospectuses + 2 synthetic Nordic-style term sheets = **12 documents**.

**Selection criteria:**
- All real documents public on SEC EDGAR — free, redistributable.
- Mix of instrument types: IPO · follow-on equity · convertible bond.
- Mix of sectors (no single-sector clustering).
- All filed 2024–2025 to keep terms recent.
- IPOs cover three filing formats commonly seen: tech / software (Reddit, Astera Labs, ServiceTitan), AI-healthcare (Tempus AI), and REIT (Lineage) — REIT IPO has materially different disclosure structure.
- Follow-ons span insurance (Gallagher), AI tech growth (SoundHound), and precision-semis (SiTime) — three different scenarios for follow-on context.
- Convertibles deliberately mid-cap to test full-feature convertible terms (capped calls, make-whole, fundamental-change, conversion mechanics).

---

## Group A — IPO prospectuses (5)

### Pick 1 — Reddit, Inc. (Social / digital advertising)

| Field | Value |
|---|---|
| Issuer | Reddit, Inc. |
| Ticker | RDDT (NYSE) |
| CIK | 0001713445 |
| Filed | 2024-03-21 |
| Form | 424B4 (final prospectus) |
| Accession | 0001628280-24-012380 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1713445/000162828024012380/reddit-final424b4.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** highly-watched 2024 tech IPO; complex revenue narrative (advertising + data licensing to LLMs); dual-class voting structure; primary + secondary tranches; lock-up arrangements with founders.

### Pick 2 — Astera Labs, Inc. (Semis / connectivity)

| Field | Value |
|---|---|
| Issuer | Astera Labs, Inc. |
| Ticker | ALAB (Nasdaq) |
| CIK | 0001736297 |
| Filed | 2024-03-21 |
| Form | 424B4 |
| Accession | 0001193125-24-073873 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1736297/000119312524073873/d285484d424b4.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** AI-infrastructure semi exposure; rapid revenue scale-up disclosure; tests LLM ability to extract from a high-growth, narrow-disclosure issuer.

### Pick 3 — Tempus AI, Inc. (Healthcare / AI)

| Field | Value |
|---|---|
| Issuer | Tempus AI, Inc. |
| Ticker | TEM (Nasdaq) |
| CIK | 0001717115 |
| Filed | 2024-06-17 |
| Form | 424B4 |
| Accession | 0001193125-24-161989 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1717115/000119312524161989/d221145d424b4.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** dual revenue stream (diagnostics services + data licensing); complex regulatory environment for healthcare AI; tests extraction from cross-domain (healthcare + AI) risk-factor disclosure.

### Pick 4 — Lineage, Inc. (REIT / cold storage)

| Field | Value |
|---|---|
| Issuer | Lineage, Inc. |
| Ticker | LINE (Nasdaq) |
| CIK | 0001868159 |
| Filed | 2024-07-26 |
| Form | 424B4 |
| Accession | 0001193125-24-185331 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1868159/000119312524185331/d577649d424b4.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** REIT IPO has structurally different prospectus disclosure (FFO/AFFO discussion, REIT qualification requirements, distribution policy, property table). Tests whether LLM recognises and adapts to REIT conventions rather than forcing into a generic corporate IPO template.

### Pick 5 — ServiceTitan, Inc. (Vertical SaaS)

| Field | Value |
|---|---|
| Issuer | ServiceTitan, Inc. |
| Ticker | TTAN (Nasdaq) |
| CIK | 0001638826 |
| Filed | 2024-12-12 |
| Form | 424B4 |
| Accession | 0001193125-24-277099 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** vertical SaaS targeting trades-industry customers; complex pricing model disclosure (subscription + transaction-based revenue); useful for extracting non-standard ECM terms such as compounding-PE-ratchet arrangements with previous investors that activate upon IPO.

---

## Group B — Follow-on equity offerings (3)

### Pick 6 — Arthur J. Gallagher & Co. (Insurance broking)

| Field | Value |
|---|---|
| Issuer | Arthur J. Gallagher & Co. |
| Ticker | AJG (NYSE) |
| CIK | 0000354190 |
| Filed | 2024-12-09 |
| Form | 424B5 |
| Accession | 0001193125-24-272966 |
| Document URL | https://www.sec.gov/Archives/edgar/data/354190/000119312524272966/d911688d424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** large IG-rated insurance broker doing a primary follow-on, likely tied to acquisition financing — tests extraction of acquisition-related use-of-proceeds disclosure on the equity side (vs. W1's debt-side equivalents).

### Pick 7 — SoundHound AI, Inc. (Voice AI)

| Field | Value |
|---|---|
| Issuer | SoundHound AI, Inc. |
| Ticker | SOUN (Nasdaq) |
| CIK | 0001840856 |
| Filed | 2024-11-08 |
| Form | 424B5 |
| Accession | 0001213900-24-095982 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1840856/000121390024095982/ea0220456-424b5_sound.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** growth-stage AI name doing a market-window follow-on; classic dilution-vs-runway tension that an LLM should recognise in the use-of-proceeds and risk factors.

### Pick 8 — SiTime Corporation (Precision timing / semis)

| Field | Value |
|---|---|
| Issuer | SiTime Corporation |
| Ticker | SITM (Nasdaq) |
| CIK | 0001451809 |
| Filed | 2025-06-26 |
| Form | 424B5 |
| Accession | 0001193125-25-149105 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1451809/000119312525149105/d33879d424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** specialty semi name; tests extraction in a niche-but-real ECM context; provides 2025 vintage to balance the otherwise 2024-heavy corpus.

---

## Group C — Convertible notes prospectuses (2)

### Pick 9 — EchoStar Corporation (Telecom / satellite — multi-entity)

| Field | Value |
|---|---|
| Issuer | EchoStar Corporation |
| Other parties | DBSD Corp; SNR Wireless (co-issuers / guarantors) |
| Ticker | SATS (Nasdaq) |
| CIK | 0001415404 (primary) + others |
| Filed | 2024-11-12 |
| Form | 424B5 (convertible) |
| Accession | 0001104659-24-116104 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1415404/000110465924116104/tm2426686-3_424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** multi-entity convertible structure (rare and tricky); tests LLM ability to identify the issuer's actual contractual obligor entity. EchoStar's complex spectrum-asset history adds risk-factor texture.

### Pick 10 — AeroVironment Inc. (Defence tech / drones)

| Field | Value |
|---|---|
| Issuer | AeroVironment Inc. |
| Ticker | AVAV (Nasdaq) |
| CIK | 0001368622 |
| Filed | 2025-07-03 |
| Form | 424B5 (convertible) |
| Accession | 0001104659-25-065459 |
| Document URL | https://www.sec.gov/Archives/edgar/data/1368622/000110465925065459/tm2519048-7_424b5.htm |
| Verified | 2026-05-12 — HTTP 200 |

**Why this one:** defence-tech sector adds diversity beyond software / consumer / financial issuers; convertible structure tests full extraction of conversion mechanics (capped call, fundamental change, anti-dilution) on a single-issuer instrument.

---

## Synthetic supplement (2 documents)

Located in `corpus/W5_ecm_terms/synthetic/`:

| File | Style mirrored | Why kept |
|---|---|---|
| `ipo_01_aurora_marine.md` | Norwegian-law Oslo Børs IPO of a fictional offshore-wind installation business | I authored — byte-perfect ground truth for primary/secondary tranche split, cornerstones, greenshoe, lock-up, and Nordic-specific governance disclosure (Norwegian Code of Practice for Corporate Governance). |
| `conv_01_borealis_quantum.md` | USD 144A / RegS convertible senior notes of a fictional Swedish quantum-tech issuer | I authored — byte-perfect ground truth for conversion-rate vs. conversion-price distinction, capped call mechanics, sale-price / trading-price conversion conditions, fundamental change make-whole. |

The two synthetics are explicitly flagged as fictional in their headers; they are not used in the paper as real-deal evidence.

---

## Sector coverage across the 10 real picks

Social media / advertising · Semis & AI-connectivity · Healthcare-AI · REIT (cold storage) · Vertical SaaS · Insurance broking · Voice AI · Precision semis · Telecom / satellite · Defence tech. Ten different sectors across ten documents — no clustering.

---

## Open follow-ups

1. Verify primary documents resolve on a fresh evaluation-time fetch (verified 2026-05-12 in this session).
2. The follow-on picks (Gallagher, SoundHound, SiTime) and the convertible picks (EchoStar, AeroVironment) — none of these are Nordic. The Nordic angle is carried by the two synthetics and (in W3) by Spotify.
3. **Advisory-conflict optics check** — confirm none of the 10 real ECM issuers had a syndicate role for the author's employer on the specific transaction listed. US tech / AI / REIT issuers are unlikely overlaps, but worth a 30-second sanity check on the author's side.

---

*Compiled 2026-05-12. URLs verified by curl with deterministic EDGAR pattern + 424B4 / 424B5 full-text search.*
