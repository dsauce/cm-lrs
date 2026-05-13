# CM-LRS — Capital Markets LLM Reliability Score

> *A 7-dimension reliability scorecard for LLM outputs in capital-markets workflows.*

This repository is the public companion release for the arXiv paper:

**Ahuja, P. (2026). _Capital Markets LLM Reliability Score (CM-LRS): From Plausible to Bankable._**

Paper PDF and LaTeX source are in [`paper/`](paper/).

## What is CM-LRS

A reliability metric that scores LLM outputs at the **workflow-output layer** (the layer bankers, analysts, and compliance reviewers actually defend) rather than the question–answer pair layer that current benchmarks evaluate. Seven dimensions, each scored 0–5:

| # | Dimension | Question it answers |
|---|---|---|
| D1 | Factual Accuracy | Are the stated facts correct against the source document? |
| D2 | Evidence Traceability | Are claims linked to specific passages, sections, or pages? |
| D3 | Numerical Consistency | Are numbers extracted correctly and internally consistent? |
| D4 | Workflow Completeness | Did the model complete all requested fields / steps? |
| D5 | Source Discipline | Did the model avoid unsupported assumptions or hallucinations? |
| D6 | Decision Usefulness | Is the output practically useful to a banker, analyst, or reviewer? |
| D7 | Reviewability | Can a human reviewer quickly verify the output and reasoning trail? |

The aggregate CM-LRS is the equal-weighted mean across the seven dimensions. Workflow-class default weights are discussed in the paper §4.

## Repo layout

```
.
├── paper/                       PDF + LaTeX source for the arXiv paper
├── corpus/                      All evaluation documents (public SEC filings + synthetic)
│   ├── W1_debt_terms/           DCM transaction-terms extraction
│   ├── W2_precedent_retrieval/  Cross-document retrieval
│   ├── W3_issuer_profile/       Issuer profile synthesis
│   ├── W4_transaction_comparable/  M&A merger-proxy / take-private documents
│   └── W5_ecm_terms/            ECM transaction-terms extraction
├── eval/                        Evaluation pipeline (Python)
│   ├── README.md                pipeline details
│   ├── preprocess.py            HTML → 6K-token clean text
│   ├── prompts.py + prompts/    workflow + judge prompt templates
│   ├── llm_clients.py           provider routing (Claude via raicode, GPT-5.5 via Codex CLI, Llama via Groq)
│   ├── runner.py                generation orchestrator (idempotent)
│   ├── scorer.py                primary LLM-as-judge scorer — Sonnet 4.6 (idempotent)
│   ├── scorer_gpt5.py           second judge — GPT-5.5 (in-panel cross-check)
│   ├── scorer_haiku.py          third judge — Claude Haiku 4.5 (out-of-panel, same family)
│   ├── scorer_gemini.py         fourth judge — Gemini 2.5 Pro (out-of-panel, different family)
│   ├── verify_numbers.py        deterministic recompute of every numeric claim in the paper
│   ├── aggregate.py             per-cell mean → scoring_table.{md,json}
│   ├── patch_paper.py           writes §7 table + failure paragraph into paper/CM_LRS_arXiv_Paper.tex
│   ├── finalize.sh              aggregate + patch in one shot
│   ├── preprocessed/<wf>/       cleaned-text inputs (one .txt per document)
│   ├── outputs/<wf>_<model>.jsonl   raw model outputs (one row per call)
│   ├── scores/<wf>_<model>.jsonl    primary-judge (Sonnet) scores
│   ├── scores_gpt5judge/<wf>_<model>.jsonl     second-judge (GPT-5.5) scores
│   ├── scores_haikujudge/<wf>_<model>.jsonl    third-judge (Haiku) scores
│   ├── scores_geminijudge/<wf>_<model>.jsonl   fourth-judge (Gemini) scores
│   ├── cross_judge_summary.md   four-way per-cell comparison + Spearman/Pearson statistics
│   ├── scoring_table.md         final aggregated table (human-readable)
│   ├── scoring_table.json       final aggregated table (machine-readable)
│   └── .env.example             credential template — copy to .env and fill in
├── LICENSE                      CC BY 4.0
├── NOTICE                       what is licensed how
└── README.md                    this file
```

## Headline results — five workflows × four models, four-judge averaged

| Workflow | Claude Opus 4.7 | GPT-5.5 | Claude Sonnet 4.6 | Llama 3.3 70B |
|---|---:|---:|---:|---:|
| W1 — DCM extraction | 4.80 | 4.62 | **4.95** | 4.11 |
| W2 — Precedent retrieval | 4.57 | 4.71 | 4.74 | 2.51 |
| W3 — Issuer profile | 4.00 | **4.48** | 4.05 | 2.33 |
| W4 — M&A comparable | **4.68** | 4.18 | **4.68** | 3.46 |
| W5 — ECM extraction | 4.48 | 4.19 | **4.76** | 3.76 |
| **Primary-judge mean** | 4.51 | 4.44 | **4.64** | 3.24 |
| **4-judge averaged mean** | **4.30** | 4.09 | **4.31** | 3.15 |

The per-workflow rows are primary-judge per-cell scores. The two summary rows show the same models under (a) the primary judge (Sonnet 4.6 acting as evaluator) and (b) the four-judge averaged means across Sonnet 4.6, GPT-5.5, Haiku 4.5, and Gemini 2.5 Pro — three model families. The three frontier closed-source models cluster within 0.22 points on the four-judge averaged view; the open-weights baseline is last under every judge.

See `eval/scoring_table.md` for the full per-dimension breakdown across all 35 (workflow × dimension) cells per model and `eval/cross_judge_summary.md` for the four-way per-cell comparison and inter-judge agreement statistics.

## Verifying the numbers

Every numeric claim in the paper is reproducible from the raw judge JSONLs:

```bash
python3 eval/verify_numbers.py
```

The script recomputes Table 1 per-cell aggregates, Table 4 cost-table means, the four-judge averaged per-model means, the open-weights gap statistics, the pairwise Spearman correlations on per-cell aggregates, and the per-dimension Pearson correlations across the six judge pairs, then prints OK/FAIL for each claim against the paper text. The current paper passes all 51 checks.

## Reproducing the evaluation

```bash
# 1. Clone and enter the repo
git clone https://github.com/dsauce/cm-lrs.git
cd cm-lrs

# 2. Set up credentials
cp eval/.env.example eval/.env
# Edit eval/.env to add your RAICODE_KEY, GROQ_KEY, GEMINI_KEY
# (GPT-5.5 via Codex CLI uses ChatGPT-account auth - run `codex login` once)

# 3. Install Python dependencies
pip install openai beautifulsoup4 tiktoken

# 4. Run the pipeline (idempotent — restart-safe at every step)
python3 eval/preprocess.py             # corpus → cleaned text
python3 eval/runner.py                 # generates outputs for all five workflows × four models
python3 eval/scorer.py                 # primary-judge scoring (Sonnet 4.6)
python3 eval/scorer_gpt5.py            # second-judge cross-check (GPT-5.5)
python3 eval/scorer_haiku.py           # third-judge cross-check (Haiku 4.5)
python3 eval/scorer_gemini.py          # fourth-judge cross-check (Gemini 2.5 Pro)
python3 eval/verify_numbers.py         # recompute every paper claim
bash eval/finalize.sh                  # aggregates + patches the paper's §7 table
```

The full primary-judge pipeline ran in ~50 minutes wall time on the eval that produced the headline tables above. The three additional judges add roughly the same wall-clock again. Total out-of-pocket cost was approximately US$1 across all four judges and all four panel models combined.

## Extending the work

The evaluation is workflow-agnostic and model-agnostic:

- **Adding a workflow:** drop documents under `corpus/W6_yourworkflow/`, add a prompt template in `eval/prompts.py`, add a sample list to `eval/runner.py`, rerun.
- **Adding a model:** add a provider client in `eval/llm_clients.py` (return text from `call_<provider>(prompt, system)`), add to the `MODELS` dict, rerun.
- **Replacing the LLM-as-judge with human raters:** read `eval/scores/*.jsonl` schema, score by hand, write rows with the same shape. `aggregate.py` is judge-agnostic.

## Citation

```bibtex
@article{ahuja2026cmlrs,
  title   = {Capital Markets LLM Reliability Score (CM-LRS): From Plausible to Bankable},
  author  = {Ahuja, Prerit},
  year    = {2026},
  journal = {arXiv preprint}
}

@misc{cmlrs2026repo,
  title  = {cm-lrs: companion code release for ``CM-LRS''},
  author = {Ahuja, Prerit},
  year   = {2026},
  howpublished = {\url{https://github.com/dsauce/cm-lrs}}
}
```

## Licence

CC BY 4.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
