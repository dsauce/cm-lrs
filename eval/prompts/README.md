# Evaluation prompts

These prompts are the canonical templates used in the CM-LRS paper's evaluation. They are programmatically defined in `eval/prompts.py` and exported here as plain-text files for direct reference in the paper and GitHub repo.

## Files

| File | Workflow |
|---|---|
| `w1_dcm_extraction.md` | W1: DCM transaction-terms extraction (bond prospectus → structured table) |
| `w2_precedent_retrieval.md` | W2: Cross-document retrieval over a 10-document corpus + 5 queries |
| `w3_issuer_profile.md` | W3: Issuer profile synthesis from 10-K / 20-F |
| `w4_transaction_comparable.md` | W4: M&A merger-proxy term extraction |
| `w5_ecm_extraction.md` | W5: ECM transaction-terms extraction (IPO / follow-on / convertible) |
| `judge.md` | LLM-as-judge prompt — scores model outputs against 7-dimension rubric |

## CM-LRS rubric

Each model output is scored on seven dimensions (0–5 each):

1. Factual Accuracy
2. Evidence Traceability
3. Numerical Consistency
4. Workflow Completeness
5. Source Discipline
6. Decision Usefulness
7. Reviewability

Anchors are defined in the paper §4.2 and reproduced verbatim in the judge prompt.

## Reproducibility

Inputs: documents in `corpus/` (preprocessed via `eval/preprocess.py` to a 6,000-token budget per document).
Models: Claude Opus 4.7, Claude Sonnet 4.6, GPT-5.5, Llama 3.3 70B Instruct.
Outputs: `eval/outputs/<workflow>_<model>.jsonl` (one row per generation, idempotent).
Scores: `eval/scores/<workflow>_<model>.jsonl` (one row per scored generation, idempotent).
Aggregates: `eval/scoring_table.md` and `eval/scoring_table.json`.
