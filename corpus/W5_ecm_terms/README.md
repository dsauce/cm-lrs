# W5 — Equity Capital Markets (ECM) Transaction Terms Extraction

**What this workflow tests.** Given an ECM prospectus or term sheet (IPO, follow-on equity offering, convertible bond), the LLM extracts and normalises the commercial terms into a structured table. Typical fields: issuer, instrument type, offering size (primary / secondary split, greenshoe), pricing (range, final price or premium), use of proceeds, underwriter syndicate, lock-up arrangements, listing exchange, distribution format (S-registered vs 144A/RegS), key bondholder protections for convertibles (conversion rate, fundamental change, make-whole, capped calls), greenshoe mechanics, stabilisation, and selected risk factors.

**Why this matters in capital markets.** ECM document extraction sits alongside DCM as the other half of "capital markets" in any pitch deck, IC memo or banker's daily workflow. The failure modes are different from DCM:

- Conflating bookbuilding price range with final pricing.
- Missing greenshoe / over-allotment mechanics or misinterpreting the size impact.
- Incorrectly extracting conversion rates vs. conversion prices on convertibles (a recurring trap).
- Misreading 144A / Regulation S distribution restrictions as "no US offering at all".
- Mistaking secondary-tranche proceeds (to the Selling Shareholder) for primary proceeds (to the Issuer).
- Missing capped-call structure on convertibles entirely.

**CM-LRS dimensions exercised most heavily:** factual accuracy, numerical consistency, evidence traceability, source discipline.

**Symmetric design with W1.** This workflow mirrors W1 (debt-terms extraction) in shape — single-document extraction with a structured-table output. Together W1 and W5 cover both legs of capital markets transactions extraction (DCM and ECM). Same scoring template; different document types.

## Folder contents

| File | What it is |
|---|---|
| `ecm_picks.md` | The ten real EDGAR documents chosen (5 IPOs + 3 follow-ons + 2 convertibles), with URLs and verification notes. |
| `synthetic/ipo_01_aurora_marine.md` | Synthetic Norwegian-law Oslo Børs IPO of a fictional offshore-wind installation business. Tests primary / secondary split, cornerstones, lock-up. |
| `synthetic/conv_01_borealis_quantum.md` | Synthetic USD 144A / RegS convertible senior notes of a fictional Swedish quantum-computing technology issuer. Tests conversion rate / price, fundamental change, make-whole, capped call. |

## Document count

| Source | Count | Files |
|---|---:|---|
| EDGAR — IPO 424B4 prospectuses | 5 | Reddit, Astera Labs, Tempus AI, Lineage, ServiceTitan |
| EDGAR — Follow-on 424B5 prospectuses | 3 | Arthur J. Gallagher, SoundHound AI, SiTime |
| EDGAR — Convertible notes 424B5 prospectuses | 2 | EchoStar, AeroVironment |
| Synthetic Nordic-style term sheets | 2 | Aurora Marine IPO, Borealis Quantum convertible |
| **Total** | **12** | |

## At evaluation time

For each of the twelve documents, the LLM is prompted with an ECM-specific extraction template (defined in the GitHub repo `prompts/w5_extract_ecm.md`, distinct from W1's debt template). Outputs are scored against the 7-dimension rubric, with a gold-standard table compiled from the synthetics (byte-perfect) and from a careful read of the real prospectuses.
