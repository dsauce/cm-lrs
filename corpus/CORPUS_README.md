# Corpus folder — file layout for review

**Updated:** 2026-05-13 v3 — **full freeze complete, Darktrace included**. Every document referenced in every picks file is now on disk locally. Total corpus is ~115 MB across 110 files. The folder is reproducibility-ready: it can be zipped, uploaded to GitHub (well within the 1 GB repo guidance), and forms the canonical version-of-record for the CM-LRS paper.

## How to review

Each workflow folder follows the same pattern:

```
corpus/
├── CORPUS_README.md             ← this file (file layout)
├── LOG.md                       ← chronological decisions log
├── W1_debt_terms/
│   ├── README.md                ← what this workflow tests
│   ├── edgar_picks.md           ← picks file (table of URLs + rationale)
│   ├── edgar/                   ← actual downloaded EDGAR HTML files
│   │   ├── 01_hca_2024-08-09.htm
│   │   └── …
│   └── synthetic/               ← markdown synthetics (authored)
│       ├── ts_01_nordhavn_industri.md
│       └── …
├── W2_precedent_retrieval/      ← same shape; edgar/ has 27 EDGAR HTMLs
├── W3_issuer_profile/           ← same shape; edgar/ has 5 annuals + 5 quarterlies + 1 exhibit
├── W4_transaction_comparable/   ← target/ has 2 deal docs; 20-comp universe deferred
└── W5_ecm_terms/                ← same shape; edgar/ has 10 ECM HTMLs
```

To open any document: just double-click the `.htm` file — it renders in a browser as the original EDGAR prospectus / annual report.

## What is on disk

| Workflow | Local files | Files | Size |
|---|---|---:|---:|
| W1 | 15 EDGAR HTMLs (bond prospectuses) + 3 synthetic .md = | **18** | **11 MB** |
| W2 | 27 EDGAR HTMLs (15 hardlinked from W1 + 12 unique) | **27** | **18 MB** |
| W3 | 5 annuals + 5 quarterlies + 7 earnings filings (announcement 8-K/6-K + Ex-99 exhibits) | **17** | **24 MB** |
| W4 | Target: Synopsys S-4/A + Ansys DEFM14A. Comparables: 19 DEFM14A / SC 13E-3 / 8-K merger filings + 1 Darktrace IR announcement HTML (deal #16). | **23** | **51 MB** |
| W5 | 10 EDGAR HTMLs (IPO + follow-on + convertible) + 2 synthetic .md | **12** | **23 MB** |
| **Total** | | **96 unique + 13 hardlinks = 109 file paths** | **~115 MB** |

## Darktrace note — included via IR announcement HTML (Path A)

Deal #16 (Thoma Bravo / Darktrace plc, US$5.3 bn, April 2024) is a UK take-private. UK schemes do not produce a US-style DEFM14A; the equivalent document is a Scheme Document hosted on the target's IR site behind a UK-eligible-investor disclaimer gate. Path-A approach taken (2026-05-13): saved the publicly accessible 23 May 2024 IR announcement HTML page (`16_darktrace_scheme_announcement_2024-05-23.htm`, 100 KB) — equivalent in shape to the Adobe/Figma 8-K announcement (deal #17) already in the corpus. The full Scheme Document PDF (~200 pages) was not retrieved because it sits behind the IR microsite disclaimer; Path B (manual download) was attempted but the disclaimer redirected to a generic FCA page. The announcement contains the deal terms, advisor list, indicative timetable and pointers to the full Scheme Document for any reader who wants to dig further. **All 20 W4 comparable deals are now on disk.**

## Why the file path count (109) exceeds unique-document count (96)

W2's `edgar/` folder contains 15 hard-links to files that physically live in W1's `edgar/` folder (the 5 original W1 picks plus the 10 W1 expansion picks that also belong to the W2 corpus). Hardlinks count as separate file paths in `find` and `ls -l`, but they take zero additional disk space and refer to the same byte stream — change the W1 copy and the W2 copy changes automatically.

## GitHub upload considerations

- **Total size (~115 MB)** is well within GitHub's 1 GB repo recommendation. No file exceeds the 100 MB single-file limit (largest is Lineage IPO at 6.6 MB).
- **No binary blobs** — everything is HTML or Markdown, which diffs cleanly and compresses well.
- **Hardlinks may not survive `git add`** on some Windows/WSL configurations. If GitHub picks up the W2 hardlinks as separate files, the repo will physically duplicate ~5 MB. That's fine.
- **License plumbing:** the EDGAR HTMLs are public-record SEC filings — redistributable. The synthetic term sheets are CC BY 4.0 by the paper's overall license. Add a `LICENSE` and `NOTICE` at the repo root before publishing.

## Document format note

All downloaded files are **HTML** (`.htm`), which is the native EDGAR-filed format for prospectuses, 10-Ks, 20-Fs, and merger proxies. EDGAR does not issue PDFs as the primary document for these filings — the HTML versions are the official public record. Modern browsers render them fine; LaTeX / pandoc can convert if PDFs are needed downstream.

The synthetic term sheets are markdown (`.md`) by design — they're authored content, not filed documents.

## Re-download

If any file gets corrupted or you want a fresh pull, all download commands are in this session's bash history. The full URL list for any workflow is in its picks file (`edgar_picks.md`, `ecm_picks.md`, etc.).
