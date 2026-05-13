# W3 — Issuer Profile

**What this workflow tests.** Given a small set of disclosure documents from one issuer (annual report, quarterly report, latest investor presentation), the LLM produces a structured issuer profile: business model and segments, geographic and customer mix, capital structure, recent financial trajectory, key risk factors, ESG positioning. Every claim must be tied to a specific source passage.

**Why this matters in capital markets.** Issuer profiles sit at the front of every credit memo, pitch deck, target screen, and IC presentation. Bankers and analysts produce them constantly. The failure mode is not just speed: it is also factual drift — quoting last year's number, inheriting peer-comp framing that doesn't apply, or omitting a risk factor the LLM treats as boilerplate but a reviewer would treat as material.

**CM-LRS dimensions exercised most heavily:** workflow completeness, source discipline, decision usefulness, reviewability.

## Folder contents

| File | What it is |
|---|---|
| `issuer_picks.md` | The 3 issuers chosen (Tesla, Equinix, Spotify), with their annual filing URLs and CIKs. |

## At evaluation time

For each of the 3 issuers, the LLM is given the same profile template (defined in the GitHub repo `prompts/w3_profile.md`) and three documents: annual report, latest quarterly, latest earnings-deck filing. Outputs are scored against the 7-dimension rubric.
