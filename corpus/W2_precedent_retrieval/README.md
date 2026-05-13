# W2 — Precedent Retrieval

**What this workflow tests.** Given a multi-document corpus and a retrieval query, the LLM must (a) identify which documents match, (b) cite the specific clause or passage in each match, and (c) provide a short comparative synthesis. The test is whether the LLM can stay disciplined as the search space grows beyond a single document.

**Why this matters in capital markets.** Precedent-pulling is a daily task in DCM, syndicated lending, and legal advisory work — "show me change-of-control puts in recent Nordic HY", "find leverage-based ratchet clauses in last year's TLB market", "compare carve-outs for permitted disposals in the prior issuances of this issuer's peers". Failure modes include missing documents, citing the wrong document, inventing clauses, or mis-summarising.

**CM-LRS dimensions exercised most heavily:** evidence traceability, workflow completeness, source discipline. Numerical consistency on Q2 specifically.

## Folder contents

| File | What it is |
|---|---|
| `corpus_list.md` | The 30 documents in the corpus (27 EDGAR + 3 synthetic), with CIKs, accessions, and URL patterns. |
| `queries.md` | The 5 retrieval queries with their CM-LRS dimension mapping and ground-truth scoring notes. |

## At evaluation time

The 27 EDGAR documents are pulled fresh using the predictable filing-index URL pattern. The 3 synthetics are read from `corpus/W1_debt_terms/synthetic/`. The 5 queries are run against each of the 4 models in the evaluation panel; outputs are scored individually against the 7-dimension rubric.
