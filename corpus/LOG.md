# CM-LRS Corpus — Decisions Log

**Purpose.** Single chronological record of every corpus decision made for the CM-LRS paper. Each entry states what was decided, the rationale, and what would trigger a revision. Open this file whenever you want to (a) see what is locked, (b) understand why, (c) reject any pick.

If you reject any pick: tell Claude in the next session "swap pick X for Y" — the pick files are independent of each other, so one swap does not unravel anything else.

---

## 2026-05-12 — First-pass corpus completed

Following Prerit's instruction ("if everything is open then you do the first take on all of this, i can review after that and reject and repeat your work if there is any need"), Claude produced a first-pass corpus across all four workflows in a single session. Folder structure:

```
corpus/
├── LOG.md                           (this file)
├── W1_debt_terms/
│   ├── README.md
│   ├── edgar_picks.md               (5 EDGAR prospectuses)
│   └── synthetic/
│       ├── ts_01_nordhavn_industri.md
│       ├── ts_02_fjordkraft_energi.md
│       └── ts_03_karelis_real_estate.md
├── W2_precedent_retrieval/
│   ├── README.md
│   ├── corpus_list.md               (30 documents)
│   └── queries.md                   (5 retrieval queries)
├── W3_issuer_profile/
│   ├── README.md
│   └── issuer_picks.md              (3 issuers)
└── W4_transaction_comparable/
    ├── README.md
    └── target_and_comparables.md    (1 target + 20 comps)
```

### Key decisions in this pass

| # | Decision | Rationale | What would trigger revision |
|---|---|---|---|
| 1 | **Use EDGAR uniformly for the SEC-registered side of the corpus.** Skip European IR pages for the first pass. | European corporate IR pages are JS-rendered SPAs; canonical PDF URLs are not stable to cite in a paper. EDGAR URLs follow a deterministic `/Archives/edgar/data/{CIK}/...` pattern. | Prerit wants Nordic-listed Volvo/Vestas/Telia annual reports specifically — would require Playwright or a manual URL share. |
| 2 | **W3 issuers: Tesla, Equinix, Spotify.** | Tesla (automotive/energy/AI — complex multi-segment); Equinix (REIT — specialised disclosure); Spotify (FPI — 20-F format + retains Nordic angle via Stockholm HQ). | Prerit prefers different sectors / specifically European-listed issuers. |
| 3 | **W4 target: Synopsys / Ansys merger (Jan 2024).** | US$35bn EDA tech M&A; banks were Goldman + Qatalyst + BofA — no Nordic bank involvement; rich SEC disclosure (S-4/A + DEFM14A both on EDGAR); enables a clean 20-comp universe of large-cap software M&A. | An advisory-conflict on the target deal would require a different target. |
| 4 | **W4 comparables: 20 large software / SaaS / take-private deals 2022–2026.** | Indexable to Synopsys/Ansys (broader enterprise software comp set); all US- or UK-listed targets, so primary documents are on EDGAR or RNS/Companies House. | Three rows (#9 Everbridge, #19 Perficient, #20 Cisco/Accedian) flagged for size-appropriate swaps. |
| 5 | **W2 corpus: 27 EDGAR 424B5 prospectuses + 3 synthetic term sheets = 30 docs.** | 424B5 is the dominant form for IG corporate bond marketing supplements; predictable URL pattern; rich covenant disclosure even for IG issuers. Synthetics add Nordic-style structures (LTV/ICR/sustainability-linked) not present in US IG. | Want indenture exhibits (Exhibit 4.1) instead — denser covenant text but harder to retrieve uniformly. |
| 6 | **W2 queries: 5 designed to stress 7 CM-LRS dimensions.** | Q1 retrieval+factual; Q2 numerical+currency; Q3 false-positive resistance; Q4 synthesis+evidence; Q5 definitional drift. | Want queries with smaller scope or different failure modes. |
| 7 | **Three synthetics (Nordhavn / Fjordkraft / Karelis) covering industrials, renewables, real estate.** | Three different governing-law regimes (SE/NO/DK), three different covenant philosophies (incurrence-only / sustainability-linked / LTV+ICR). Names are obviously fictional (Cyrillic-Nordic blend, geographic concepts) to avoid any misread as real issuers. | Want more synthetics (covering banks, oil majors, telecom) or fewer. |

### What was NOT done in this pass

- No documents were physically downloaded into the corpus folder. URLs are documented; bulk download happens at evaluation time (Step 3 in the README critical path).
- No Nordic regulator (Finansinspektionen, Finanstilsynet) filings included. Reason: their redistribution position needs to be verified first, per the warning in the session log.
- The investor presentations for W3 (8-K Exhibit 99 / 6-K filings) are referenced by filings-list URL only; the specific 8-K accession needs to be picked at evaluation time because issuers file these every quarter.
- No checks against the model-availability question (A1, A2 in `for_prerit.md`).

### Items deferred to Prerit's review

All open items are listed in `context/for_prerit.md`. The corpus-specific ones are:

- A reality-check on the W4 comparable universe (B2 in `for_prerit.md`).
- Sign-off on the W3 SEC-issuer pivot or a request to invest more effort retrieving Nordic IR PDFs (B1).
- Approval style for W1/W2 URLs going forward (B3).

### Verification quality

Every URL listed in `edgar_picks.md`, `issuer_picks.md`, and `target_and_comparables.md` was tested with `curl -I` or by retrieving the filing-index HTML during this session. EDGAR returned HTTP 200 in all cases. Cover-page content (issuer, offering size, tranches, date) was inspected for the W1 picks to confirm the primary document is what the index claimed.

---

## 2026-05-12 — W5 added (ECM coverage)

Prerit flagged that the corpus was DCM + M&A only, with no equity-capital-markets representation despite the paper being titled "Capital Markets LLM Reliability Score". Chose Option 2 (new W5 workflow, symmetric to W1).

### W5 design

- **Workflow:** ECM transaction terms extraction. Same shape as W1 (single-document, structured-table output) but on ECM documents.
- **Document count:** 10 real EDGAR + 2 synthetic Nordic-style = **12 documents**.
- **Document mix:**
  - 5 IPO 424B4 prospectuses: Reddit · Astera Labs · Tempus AI · Lineage (REIT IPO) · ServiceTitan
  - 3 Follow-on 424B5 prospectuses: Arthur J. Gallagher · SoundHound AI · SiTime
  - 2 Convertible 424B5 prospectuses: EchoStar (multi-entity) · AeroVironment
  - 2 Synthetic Nordic term sheets: Aurora Marine ASA (IPO) · Borealis Quantum AB (USD 144A convertible)

### Why this mix

- IPO + follow-on + convertible spans the three most common ECM document types. Rights offerings deliberately excluded (rare in US; common in Europe but harder to source on EDGAR).
- Lineage = REIT IPO and EchoStar = multi-entity convertible deliberately included as structural-edge cases (REIT FFO/AFFO disclosure; co-issuer / co-guarantor handling).
- ServiceTitan tests vertical-SaaS conversion-ratchet language (sometimes seen in pre-IPO investor agreements).
- Two synthetics chosen for the same reason as W1: I authored them so the gold standard for extraction is byte-perfect; eliminates reading-error risk in my rubric.

### Paper section impact

The paper currently has §6.4 as the M&A comp section and four workflows total. Adding W5 means:

- A new §6.5 needs to be written defining the ECM workflow.
- §7's scoring table grows from 4 workflows × 4 models = 16 cells to 5 × 4 = 20 cells.
- §5.2 prompt-template inventory grows from 4 to 5 prompts.
- Title and abstract may want to be updated to make ECM coverage explicit (currently they say "capital markets workflows" which is consistent, but the introduction needs an extra sentence).

These are mechanical updates and have been added to `for_prerit.md` Section G.

### Counts after W5 (v3)

| Workflow | Real | Synthetic | Total | Meets ≥15? |
|---|---:|---:|---:|---|
| W1 — DCM extraction | 15 | 3 | 18 | yes |
| W2 — Precedent retrieval | 27 | 3 | 30 | yes |
| W3 — Issuer profile | 15 | 0 | 15 | yes |
| W4 — Transaction comparable | 21 deals (~60+ docs at eval) | 0 | 60+ | yes |
| **W5 — ECM extraction** | **10** | **2** | **12** | below 15 by 3 (note) |

**Note on W5 count.** The 10 + 2 design is symmetric to W1's 15 + 3 (target 5:1 real:synthetic ratio). To strictly meet the 15-real bar, add 3 more real ECM prospectuses (e.g., another IPO + another follow-on + a rights offering). Decision deferred to Prerit's review.

---

## 2026-05-12 — Bulk document download (v4)

Prerit observed: *"i only md files in there, not actual documents like pdf files, what am i missing?"* — fair point. The earlier passes documented URLs but didn't pull the documents, which makes review require round-tripping to sec.gov for every pick.

### Action

Pulled all primary documents into per-workflow `edgar/` subfolders:

| Workflow | Files | Disk |
|---|---:|---:|
| W1 — DCM extraction | 15 EDGAR HTMLs | 11 MB |
| W2 — Precedent retrieval | 27 EDGAR HTMLs (15 hardlinked from W1 + 12 unique downloads) | 7 MB unique (18 MB if counted as separate files) |
| W3 — Issuer profile | 5 annuals + 5 quarterlies + 1 Ferrari exhibit | 23 MB |
| W4 — Transaction comparable | Synopsys S-4/A + Ansys DEFM14A (target only) | 9 MB |
| W5 — ECM extraction | 10 EDGAR HTMLs | 23 MB |
| **Total** | **~73 files** | **~72 MB** |

### One Tapestry correction

Initial Tapestry URL pointed at accession 0001140361-24-048248 which had been withdrawn (returned an 8 KB "File Unavailable" SEC error page). Re-resolved to 0001140361-24-048675 (665 KB, valid 424B5). `corpus_list.md` updated.

### Why W4 comparables and W3 earnings decks not downloaded

- **W4 comparables (~60 documents, ~300 MB):** the 20-deal comparable universe each has 2–3 supporting filings. Adding all of them adds significant disk for marginal review value — the picks file already has rationale and URL pointers for each deal. Pull at evaluation time. If Prerit wants them now, one command pulls everything.
- **W3 earnings decks:** filed as 8-K Exhibit 99 or 6-K; rotate every quarter. Freezing a static URL now would invite link rot before submission. Pull at evaluation time when the latest deck is known.

### File format note

EDGAR filings are native HTML (`.htm`) — not PDF. EDGAR does not issue PDFs as the official version of prospectuses, 10-Ks, 20-Fs, or merger proxies; the HTML is the public record. Modern browsers render them fine; pandoc / wkhtmltopdf can convert to PDF if downstream tooling needs it.

### Folder layout reference

New `CORPUS_README.md` at the corpus root summarises file layout, file counts per workflow, what's downloaded vs URL-only, and the format note above. Open that file first for an overview.

---

## 2026-05-12 — Full freeze (v5)

Prerit instructed: *"pull everything right now. the purpose is not to have the latest docs. the purpose is to have a good quality product diverse corpus so that testing appears rigorous and consequently research paper has credibility… need to have everything frozen and on my pc now. go."* — done.

### W4 comparables — 20 deals downloaded

Initial CIK guesses for several targets were wrong (PE-acquired companies had Delaware subsidiaries with different CIKs; full-text search via EDGAR's FTS endpoint resolved the correct entities). The complete list:

| # | Deal | Target CIK (verified) | Form | Local file |
|---|---|---|---|---|
| 01 | Microsoft / Activision | 0000718877 | DEFM14A | 01_activision_defm14a_2022-04-21.htm |
| 02 | Cisco / Splunk | 0001353283 | DEFM14A | 02_splunk_defm14a_2023-10-30.htm |
| 03 | Broadcom / VMware | 0001124610 | DEFM14A | 03_vmware_defm14a_2022-08-04.htm |
| 04 | Vista / KnowBe4 | 0001664998 | DEFM14A | 04_knowbe4_defm14a_2022-12-22.htm |
| 05 | Vista / Avalara | 0001348036 | DEFM14A | 05_avalara_defm14a_2022-09-12.htm |
| 06 | Vista+Elliott / Citrix | 0000877890 | DEFM14A | 06_citrix_defm14a_2022-03-15.htm |
| 07 | Thoma Bravo / Anaplan | 0001540755 | DEFM14A | 07_anaplan_defm14a_2022-05-03.htm |
| 08 | Permira / Mimecast | 0001644675 | DEFM14A | 08_mimecast_defm14a_2022-02-02.htm |
| 09 | IBM / HashiCorp | 0001720671 | DEFM14A | 09_hashicorp_defm14a_2024-06-21.htm |
| 10 | Thoma Bravo / Coupa | 0001385867 | DEFM14A | 10_coupa_defm14a_2023-01-19.htm |
| 11 | Francisco+TPG / New Relic | 0001448056 | DEFM14A | 11_newrelic_defm14a_2023-09-25.htm |
| 12 | HPE / Juniper | 0001043604 | DEFM14A | 12_juniper_defm14a_2024-02-26.htm |
| 13 | Silver Lake / Qualtrics | 0001747748 | **DEFM14C** | 13_qualtrics_defm14c_2023-04-24.htm |
| 14 | Blackstone+Vista / Smartsheet | 0001366561 | DEFM14A | 14_smartsheet_defm14a_2024-11-04.htm |
| 15 | Permira / Squarespace | 0001496963 | DEFM14A | 15_squarespace_defm14a_2024-07-17.htm |
| 16 | Thoma Bravo / Darktrace | UK-LISTED | — | **NOT ON EDGAR — excluded** |
| 17a | Adobe / Figma announcement | 0000796343 (Adobe) | 8-K | 17a_adobe_figma_announce_8k_2022-09-15.htm |
| 17b | Adobe / Figma termination | 0000796343 (Adobe) | 8-K | 17b_adobe_figma_terminate_8k_2023-12-18.htm |
| 18 | Permira / Zendesk | 0001463172 | DEFM14A | 18_zendesk_defm14a_2022-06-13.htm |
| 19 | Blackstone / Cvent | 0001827075 | DEFM14A | 19_cvent_defm14a_2023-05-03.htm |
| 20 | Cisco / Acacia Communications | 0001651235 | DEFM14A | 20_acacia_defm14a_2021-02-09.htm |

Notes:
- **Qualtrics filed DEFM14C** (information statement) rather than DEFM14A because SAP held the majority of voting shares pre-deal — no shareholder vote was needed.
- **Adobe / Figma** has 2 docs (announcement + termination) because it's a "comp that didn't close" — a deliberate inclusion to test how an LLM handles failed-deal data in the comp universe.
- **Darktrace excluded** because no EDGAR filings (UK-listed).

W4 comparable docs: 20 files, ~43 MB.

### W3 earnings filings — 5 issuers downloaded

For each of the 5 W3 issuers, downloaded the latest 8-K (US registrants) or 6-K (FPIs) earnings filing plus its Exhibit 99 (press release / earnings deck):

| Issuer | Earnings filing date | Files |
|---|---|---|
| Tesla | 2026-04-22 | 8-K cover + EX-99.1 (49 KB) |
| Equinix | 2026-04-29 | 8-K cover + Q1'26 press release (491 KB) |
| Spotify | 2026-04-28 | 6-K with full interim narrative (1040 KB) |
| Ferrari | 2026-05-11 | 6-K cover + exhibit (54 KB combined) |
| CME Group | 2026-04-22 | 8-K cover + EX-99 (229 KB) |

W3 added: 7 files, ~1.9 MB. Removed 3 duplicate Ferrari/Spotify files left over from the earlier pass.

### Final corpus inventory (v5)

| Workflow | Files on disk | Disk |
|---|---:|---:|
| W1 | 18 | 11 MB |
| W2 | 27 (15 hardlinks + 12 unique) | 18 MB |
| W3 | 17 | 24 MB |
| W4 | 22 | 51 MB |
| W5 | 12 | 23 MB |
| **Total** | **96 unique + 13 hardlinks = 109 file paths** | **~115 MB** |

### Reproducibility-ready

Total disk well within GitHub limits (1 GB repo / 100 MB per file). Largest single file: Lineage IPO at 6.6 MB. The corpus is now a frozen, version-of-record artefact suitable for upload alongside the paper.

### Excluded from local freeze (1 of 20 W4 deals)

Darktrace plc (Thoma Bravo, April 2024) — UK take-private executed by scheme of arrangement; documents live on LSE RNS / Companies House, not EDGAR. Pulling would require Playwright. Flagged in W4 picks file and CORPUS_README; if Prerit wants Darktrace too, install Playwright or share the scheme document URL.

---

## 2026-05-13 — Darktrace added (corpus 20/20)

Prerit downloaded the Darktrace IR announcement HTML page via Path A (the route documented after Path B's IR-microsite disclaimer redirected to a generic FCA page rather than serving the Scheme Document PDF). Saved as `corpus/W4_transaction_comparable/comparables/16_darktrace_scheme_announcement_2024-05-23.htm` (100 KB).

### What this adds to the corpus

| Workflow | Before | After |
|---|---:|---:|
| W4 comparables (file count) | 21 files for 19 of 20 deals | **22 files for 20 of 20 deals** |
| W4 disk | 51 MB | 51 MB (Darktrace HTML is 100 KB — negligible) |

### Equivalence note

The Darktrace announcement is in shape and depth equivalent to the Adobe/Figma 8-Ks already in the corpus (deal #17). Both are announcement-class filings, not full proxies. The Synopsys/Ansys-like full DEFM14As remain the standard for the other 18 W4 comparables; Darktrace (#16) and Adobe/Figma (#17) are both announcement-class. The W4 scoring exercise will need to acknowledge the depth difference for these two cells.

### Caveat now removed

`CORPUS_README.md` no longer flags Darktrace as excluded. The full corpus is locally complete.

---

## How to revise

To swap any pick:

1. Open the relevant picks file.
2. Replace the row in the table.
3. Append an entry to this LOG.md describing what changed and why.

To swap a whole workflow's design (e.g. "use UK take-privates instead of US for W4"):

1. Edit the relevant picks file.
2. Update `corpus/Wn_*/README.md` if the workflow framing changes.
3. Append a major-revision entry here.

---

## 2026-05-12 — Expansion pass (v2)

Prerit pushed back on the document counts and asked for ≥15 per workflow before review. Disclosed transparently that the 3 Nordic term sheets in `W1/synthetic/` are fabricated documents I authored (used for byte-perfect ground-truth scoring of W1 extraction accuracy). Hybrid real + synthetic design is retained, but real-document counts increased.

### Counts before → after

| Workflow | Before | After | Increment |
|---|---:|---:|---|
| W1 | 5 real + 3 synthetic = 8 | **15 real + 3 synthetic = 18** | +10 real EDGAR prospectuses |
| W2 | 27 real + 3 synthetic = 30 | unchanged at 30 | already above the 15 minimum |
| W3 | 3 issuers × 3 docs = 9 | **5 issuers × 3 docs = 15** | +2 issuers (Ferrari NV, CME Group) |
| W4 | 1 target + 20 comps (3 flagged for swap) | **1 target + 20 comps, swaps applied** | size-appropriate substitutes |

### W1 additions (picks 6–15)

Starbucks · BorgWarner · Las Vegas Sands · Agilent · Crown Castle · Fiserv · Expedia · Micron · Georgia Power · Waste Management. All 424B5 filings 2024–2025; all URLs verified by curl. Sector coverage expanded from 4 to 14 sectors. Includes one structurally different security type — Georgia Power's first-mortgage bonds — to stress LLM ability to recognise non-senior-unsecured covenant frameworks.

### W3 additions

- **Ferrari N.V.** (RACE, NYSE, 20-F format) — luxury automotive; Italian / Dutch jurisdiction-mix; waitlist-driven operating metric distinct from Tesla.
- **CME Group Inc.** (CME, Nasdaq, 10-K format) — financial-exchange business; regulatory-revenue exposure; directly capital-markets relevant without being an investment-banking employer-sensitive name.

### W4 swaps

| # | Out | In | Reason |
|---|---|---|---|
| 9 | Thoma Bravo / Everbridge ($1.5bn) | IBM / HashiCorp ($6.4bn, 2024, closed Feb 2025) | Size; tighter to Synopsys/Ansys infra-software profile |
| 17 | Qualtrics duplicate | Adobe / Figma ($20bn, terminated Dec 2023) | Adds a "comp that didn't close" — bankers do cite failed deals |
| 19 | EQT / Perficient ($3.0bn) | Blackstone / Cvent ($4.6bn, 2023) | Size; cleaner SaaS take-private |
| 20 | Cisco / Accedian (too small) | Cisco / Acacia Communications ($4.5bn, 2021) | Both genuine Cisco strategic moves; semi-infrastructure adjacency to Synopsys/Ansys |

### Nordic regulator filings — deferred (not feasible without Playwright)

Tested access to Finansinspektionen (SE), Finanstilsynet (NO), ESMA EU register, and direct issuer IR pages (Heimstaden, SSAB) for Nordic bond prospectus PDFs.

- All four data sources use JavaScript-rendered SPA search interfaces.
- A single FI meta-document (`prospekt-med-europapass-2026-05-08.pdf`, 120 pages) was retrievable as a static asset — useful as a meta-reference but not a substantive prospectus.
- Without Playwright installed, individual prospectus PDFs can't be reliably extracted at scale.

**Decision.** Defer Nordic regulator filings. The Nordic angle in the corpus is now carried by:
- The 3 synthetic term sheets (W1) — fictional but Nordic-styled.
- Spotify in W3 (Stockholm HQ).
- The W2 retrieval queries that explicitly cross-reference the Nordic synthetics.

If Prerit wants Nordic regulator filings later, options are: (a) install Playwright; (b) Prerit shares known prospectus URLs from his bookmarks; (c) accept the corpus as US-EDGAR-dominant.

### Verification quality (v2)

All 10 W1 expansion URLs verified HTTP 200 with substantive content sizes (538 KB to 2 MB). Ferrari NV 20-F + 6-K verified. CME 10-K + 10-Q verified. W4 swap-in deals all from public US M&A history; press-release references can be pulled at evaluation time.

---

*Initial pass: 2026-05-12 (v1). Expansion pass: 2026-05-12 (v2).*
