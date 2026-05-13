# W4 — Transaction Comparable

**What this workflow tests.** Given a target transaction and a corpus of public comparable deals, the LLM retrieves the most relevant comparables, extracts key deal metrics (EV, EV/EBITDA, EV/Revenue, premium to undisturbed price), and produces a synthesised comparable-transactions write-up suitable for a banker's pitch or fairness opinion appendix.

**Why this matters in capital markets.** Comparable-transactions work is one of the highest-volume, highest-stakes tasks in M&A and ECM banking. The numbers feed pricing, fairness opinions, and pitch positioning. Failure modes include: comp drift (picking deals from the wrong sector or vintage), number errors (mixing announcement-day price with completion-day metrics, getting the cap structure wrong), evidence gaps (citing a deal but not the underlying disclosure), and source confusion (quoting Refinitiv vs Mergermarket vs the actual press release).

**CM-LRS dimensions exercised most heavily:** evidence traceability, numerical consistency, decision usefulness, source discipline.

## Folder contents

| File | What it is |
|---|---|
| `target_and_comparables.md` | Target deal (Synopsys / Ansys) + 20 comparable software-M&A deals 2022–2026, with advisor list confirmation that no Nordic bank was on the target deal. |

## Constraint check

The target deal (Synopsys / Ansys) was advised by Goldman Sachs (acquirer) and Qatalyst Partners (target). The corporate-debt financing was led by US bulge-bracket banks. No Nordic bank was on the advisor list. This was confirmed against the 16 January 2024 announcement press releases and the SEC S-4 / DEFM14A.

## At evaluation time

The LLM is given the target deal documents (S-4/A + DEFM14A + announcement 8-Ks) and the 20-deal comparable universe (with documents pulled at evaluation time per the URL patterns in `target_and_comparables.md`). The output is scored against the 7-dimension rubric, with the metric-extraction tables checked against the underlying disclosures.
