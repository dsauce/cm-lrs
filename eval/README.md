# CM-LRS Evaluation Pipeline

Self-contained evaluation pipeline for the CM-LRS paper. Reproduces the §7 scoring table end-to-end given the corpus in `/corpus/`.

## Layout

```
eval/
├── README.md
├── PROGRESS_OVERNIGHT.md     ← high-level status notes
├── preprocess.py             ← HTML → cleaned text, truncate to 6K-token budget
├── prompts.py                ← Python-side prompt templates (used by runner)
├── prompts/                  ← Same prompts as standalone .md files (for repo readers)
│   ├── README.md
│   ├── w1_dcm_extraction.md
│   ├── w2_precedent_retrieval.md
│   ├── w3_issuer_profile.md
│   ├── w4_transaction_comparable.md
│   ├── w5_ecm_extraction.md
│   └── judge.md
├── llm_clients.py            ← four-provider client wrapper
├── runner.py                 ← main generation orchestrator (idempotent)
├── scorer.py                 ← LLM-as-judge orchestrator (idempotent)
├── aggregate.py              ← per-cell mean → scoring_table.{md,json}
├── patch_paper.py            ← edit §7 table + failure paragraph in CM_LRS_arXiv_Paper.tex
├── finalize.sh               ← aggregate + patch in one shot
├── preprocessed/             ← cleaned-text per document, per workflow
├── outputs/                  ← <workflow>_<model>.jsonl — one row per generation
├── scores/                   ← <workflow>_<model>.jsonl — one row per scored generation
├── logs/                     ← runner.log, scorer.log, plus per-model run logs
└── scoring_table.{md,json}   ← final aggregated table
```

## Pipeline order

```
preprocess.py  →  runner.py  →  scorer.py  →  aggregate.py  →  patch_paper.py
```

All four downstream steps are idempotent — rerun is safe and will only do new work.

## Models in this evaluation

| Short | Model | Provider | Endpoint |
|---|---|---|---|
| `opus` | Claude Opus 4.7 | Anthropic via Radical gateway | OpenAI-compatible Responses API at `https://gateway.raicode.no/v1` |
| `sonnet` | Claude Sonnet 4.6 | Anthropic via Radical gateway | Same |
| `gpt5` | GPT-5.5 | OpenAI via Codex CLI | `codex exec` non-interactive, ChatGPT-account auth |
| `llama` | Llama 3.3 70B Instruct | Meta via Groq | OpenAI-compatible Chat Completions at `https://api.groq.com/openai/v1` |

The judge model for scoring is Claude Sonnet 4.6 (same gateway).

## How to rerun a specific cell

To regenerate one (workflow, model) cell:

```bash
# Delete the rows for that cell from outputs/scores
python3 -c "
import json
path = 'outputs/W1_llama.jsonl'
keep = []
with open(path) as f:
    for line in f:
        r = json.loads(line)
        if r['doc_key'] != 'specific_doc_key_to_redo':
            keep.append(line)
open(path, 'w').writelines(keep)
"
# Then rerun the runner — it'll fill in the deleted row
python3 runner.py --workflows W1 --models llama
```

## How to add a new workflow

1. Add the workflow's preprocess directory under `corpus/`.
2. Add a sample list to `runner.py`'s `SAMPLES` dict.
3. Add a prompt template to `prompts.py` (or `W2_PROMPT` if retrieval-style).
4. Add the workflow ID to `runner.py`'s default `workflows_to_run`.
5. Rerun the pipeline.

## How to add a new model

1. Add the provider client to `llm_clients.py` (return a string from `call_<provider>(prompt, system)`).
2. Route the model ID in `call_model()`.
3. Add to `MODELS` dict.
4. Rerun `runner.py --models <new_model>` and `scorer.py`.

## Reproducibility note

All prompts, decoding parameters (temperature 0, max_tokens 4096 for Llama), preprocessing settings (6,000-token budget per document), and the rubric are deterministic and version-controlled. The four models are pinned by name; specific weights/versions may drift over time but the rubric and pipeline are model-agnostic.
