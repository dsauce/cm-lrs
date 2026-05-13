# W1 — Debt-Terms Extraction

**What this workflow tests.** Given a single bond prospectus or term sheet, the LLM extracts and normalises the commercial terms into a structured table. Typical fields: issuer, guarantors, principal, tranches, coupon, tenor, call schedule, change-of-control put, covenant headlines (incurrence test thresholds, RP basket, permitted-debt baskets), security package (if secured), governing law.

**Why this matters in capital markets.** This is among the most repetitive and error-prone manual tasks in a DCM banker's workflow. If an LLM can do it reliably and traceably, it removes hours of associate time per pitch — but unreliable extraction is worse than no extraction, because downstream pricing and credit conclusions inherit the error.

**CM-LRS dimensions exercised most heavily:** factual accuracy, numerical consistency, evidence traceability.

## Folder contents

| File | What it is |
|---|---|
| `edgar_picks.md` | The five real-world public prospectuses chosen, with URLs and verification notes. |
| `synthetic/ts_01_nordhavn_industri.md` | Synthetic Swedish-law senior secured FRN — industrials. |
| `synthetic/ts_02_fjordkraft_energi.md` | Synthetic Norwegian-law senior unsecured green FRN — renewables. |
| `synthetic/ts_03_karelis_real_estate.md` | Synthetic Danish-law senior secured FRN — real estate, LTV/ICR-based covenants. |

## At evaluation time

For each of the eight documents (5 real + 3 synthetic), the LLM is prompted with the same extraction template (defined in the GitHub repo `prompts/w1_extract.md`). Outputs are scored against the 7-dimension rubric using the gold-standard table (manually compiled from the synthetics and from a careful read of the real prospectuses).
