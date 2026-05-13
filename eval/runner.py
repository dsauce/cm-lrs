"""
Main evaluation runner.

Iterates over (workflow, model, document) triples, calls the LLM, and appends
results to outputs/<workflow>_<model>.jsonl. Idempotent: if a (workflow, model,
doc_key) result already exists in the cache, the call is skipped.

Crash-resumable: each successful generation is fsynced before continuing.

Rate limit handling for Groq: pacing between Llama calls so we stay under the
free-tier TPM/RPM.
"""

import os
import json
import time
import hashlib
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from llm_clients import call_model, MODELS
from prompts import PROMPTS, W2_PROMPT, WORKFLOW_DESCRIPTIONS

ROOT = Path("/mnt/c/Working3/arxiv1")
PREPROC = ROOT / "eval" / "preprocessed"
OUTPUTS = ROOT / "eval" / "outputs"
LOGS = ROOT / "eval" / "logs"
OUTPUTS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

PROMPT_VERSION = "v1"

# Pacing: Groq free tier is ~30 RPM and 6000 TPM. With our ~6K-token prompts
# we are right at the TPM ceiling per minute. Sleep 12s between Groq calls
# to stay well under both limits.
GROQ_PACING_S = 60  # bumped from 12 → 60 to stay within Groq free-tier TPM rolling window for W4 docs

# Document samples per workflow. We can't afford to score every doc against
# every model overnight; we sample for breadth + ground-truth coverage.
# Synthetic docs are always included (we know the gold standard).
SAMPLES = {
    # W1: 3 synthetics + 5 real picks for sector spread
    "W1": [
        "synth_ts_01_nordhavn_industri",
        "synth_ts_02_fjordkraft_energi",
        "synth_ts_03_karelis_real_estate",
        "01_hca_2024-08-09",
        "03_dell_emc_2024-10-03",
        "08_lasvegassands_2025-04-29",
        "10_crowncastle_2024-08-01",
        "14_georgiapower_2024-02-20",
    ],
    # W3: 3 of 5 issuers, just the annual report (skip quarterlies / earnings for speed)
    "W3": [
        "tesla_10K_FY2025",
        "equinix_10K_FY2025",
        "spotify_20F_FY2025",
    ],
    # W4: target docs + 3 representative comparables
    "W4": [
        "synopsys_S4A_2024-08",
        "01_activision_defm14a_2022-04-21",
        "12_juniper_defm14a_2024-02-26",
        "20_acacia_defm14a_2021-02-09",
    ],
    # W5: 2 synthetics + 4 real spanning IPO / follow-on / convertible
    "W5": [
        "synth_ipo_01_aurora_marine",
        "synth_conv_01_borealis_quantum",
        "01_reddit_ipo_2024-03-21",
        "04_lineage_ipo_2024-07-26",
        "06_gallagher_followon_2024-12-09",
        "09_echostar_conv_2024-11-12",
    ],
}

# W2 queries (from corpus/W2_precedent_retrieval/queries.md)
W2_QUERIES = {
    "Q1_CoC_put": "Identify every document in the provided corpus that contains a change-of-control put provision. For each match: (a) the put price (e.g., 101% of principal, par), (b) the threshold that triggers the put (e.g., acquisition of >50% voting rights), and (c) the section heading where the clause appears.",
    "Q2_general_basket": "Across the three synthetic Nordic term sheets in the corpus (Nordhavn Industri AB, Fjordkraft Energi Holding AS, Karelis Real Estate ApS), identify the size of the 'general basket' within the permitted-debt covenant for each. Convert all values to EUR using SEK/EUR = 11.50. Rank from largest to smallest.",
    "Q3_REIT_classify": "Identify any document in this corpus where the issuer is a real estate investment trust (REIT). For each, state the basis for your conclusion (form filed, organisational structure, explicit characterisation in the document).",
    "Q4_optional_redemption": "Compare the optional redemption schedules of the three synthetic Nordic term sheets. For each: (1) non-call period, (2) call price step-downs year by year, (3) presence of equity claw and its terms, (4) any sustainability-linked or non-standard call structure. Return as a comparison table.",
    "Q5_healthcare_classify": "Which documents in this corpus are filed by issuers in the healthcare sector? Healthcare here means hospital operators, healthcare distributors, pharma, or medical devices for patient care — exclude life-sciences instrument or research-tools companies.",
}

# W2 corpus: subset of 10 docs containing the key clauses we'll score against
W2_CORPUS_KEYS = [
    "01_hca_2024-08-09",          # healthcare provider; CoC put
    "02_netflix_2024-07-31",       # streaming
    "03_dell_emc_2024-10-03",      # co-issuer tech
    "05_cencora_2024-12-02",       # healthcare distributor
    "14_agilent_2024-09-04",       # life sciences instruments — edge case
    "17_crowncastle_2024-08-01",   # REIT — known positive
    "21_labcorp_2024-09-16",       # diagnostics — edge case
    "synth_ts_01_nordhavn_industri",
    "synth_ts_02_fjordkraft_energi",
    "synth_ts_03_karelis_real_estate",
]


def cache_key(workflow: str, model: str, doc_key: str) -> str:
    return f"{workflow}|{model}|{doc_key}|{PROMPT_VERSION}"


def output_path(workflow: str, model_short: str) -> Path:
    return OUTPUTS / f"{workflow}_{model_short}.jsonl"


def load_done_keys(path: Path) -> set:
    """Read existing JSONL output and return set of cache_keys already generated."""
    done = set()
    if not path.exists():
        return done
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
                done.add(row["cache_key"])
            except Exception:
                continue
    return done


def append_jsonl(path: Path, row: dict):
    """Append a row to a JSONL file with fsync for crash resilience."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def read_doc(workflow: str, doc_key: str) -> str:
    """Read preprocessed text for a workflow document."""
    return (PREPROC / workflow / f"{doc_key}.txt").read_text(encoding="utf-8")


def log_event(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOGS / "runner.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_workflow_standard(workflow: str, model_short: str, model_id: str, docs: list):
    """W1, W3, W4, W5 — single-document extraction prompts."""
    out_path = output_path(workflow, model_short)
    done = load_done_keys(out_path)
    prompt_template = PROMPTS[workflow]
    is_groq = (model_id == "llama-3.3-70b-versatile")

    for doc_key in docs:
        key = cache_key(workflow, model_id, doc_key)
        if key in done:
            log_event(f"SKIP cached {workflow} {model_short} {doc_key}")
            continue

        doc_text = read_doc(workflow, doc_key)
        prompt = prompt_template.format(document=doc_text)

        t0 = time.time()
        try:
            output = call_model(model_id, prompt)
            elapsed = time.time() - t0
            row = {
                "cache_key": key,
                "workflow": workflow,
                "model_id": model_id,
                "model_short": model_short,
                "doc_key": doc_key,
                "prompt_version": PROMPT_VERSION,
                "output": output,
                "elapsed_s": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "error": None,
            }
            append_jsonl(out_path, row)
            log_event(f"OK   {workflow} {model_short} {doc_key} ({elapsed:.1f}s, {len(output)} chars)")
        except Exception as e:
            elapsed = time.time() - t0
            row = {
                "cache_key": key,
                "workflow": workflow,
                "model_id": model_id,
                "model_short": model_short,
                "doc_key": doc_key,
                "prompt_version": PROMPT_VERSION,
                "output": None,
                "elapsed_s": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "error": str(e)[:500],
            }
            append_jsonl(out_path, row)
            log_event(f"FAIL {workflow} {model_short} {doc_key}: {str(e)[:200]}")

        if is_groq:
            time.sleep(GROQ_PACING_S)


def run_w2(model_short: str, model_id: str):
    """W2 — multi-document retrieval. Build the corpus context once per model,
    run all 5 queries against it. doc_key in this case is the query key."""
    out_path = output_path("W2", model_short)
    done = load_done_keys(out_path)
    is_groq = (model_id == "llama-3.3-70b-versatile")

    # Build corpus context — concatenate the 10 W2 corpus docs with clear headers
    corpus_parts = []
    for i, k in enumerate(W2_CORPUS_KEYS, 1):
        # W2 corpus docs include synthetics that live in W1's preprocessed folder
        path = PREPROC / "W1" / f"{k}.txt"
        if not path.exists():
            path = PREPROC / "W2" / f"{k}.txt"
        if not path.exists():
            log_event(f"WARN W2 corpus doc missing: {k}")
            continue
        text = path.read_text(encoding="utf-8")
        # Truncate each corpus doc more aggressively so we fit
        # All 10 docs × 3000 tokens = 30K tokens — fits in all models
        # Use first ~12K chars (~3K tokens)
        text = text[:12000]
        corpus_parts.append(f"\n\n=== DOC {i:02d} | {k} ===\n\n{text}")
    corpus_text = "".join(corpus_parts)

    for q_key, q_text in W2_QUERIES.items():
        key = cache_key("W2", model_id, q_key)
        if key in done:
            log_event(f"SKIP cached W2 {model_short} {q_key}")
            continue

        prompt = W2_PROMPT.format(query=q_text, corpus=corpus_text)

        t0 = time.time()
        try:
            output = call_model(model_id, prompt)
            elapsed = time.time() - t0
            row = {
                "cache_key": key,
                "workflow": "W2",
                "model_id": model_id,
                "model_short": model_short,
                "doc_key": q_key,
                "prompt_version": PROMPT_VERSION,
                "output": output,
                "elapsed_s": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "error": None,
            }
            append_jsonl(out_path, row)
            log_event(f"OK   W2 {model_short} {q_key} ({elapsed:.1f}s, {len(output)} chars)")
        except Exception as e:
            elapsed = time.time() - t0
            row = {
                "cache_key": key,
                "workflow": "W2",
                "model_id": model_id,
                "model_short": model_short,
                "doc_key": q_key,
                "prompt_version": PROMPT_VERSION,
                "output": None,
                "elapsed_s": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "error": str(e)[:500],
            }
            append_jsonl(out_path, row)
            log_event(f"FAIL W2 {model_short} {q_key}: {str(e)[:200]}")

        if is_groq:
            time.sleep(GROQ_PACING_S)


def main(workflows_to_run=None, models_to_run=None):
    """Run the eval. Default: all 5 workflows × 4 models."""
    if workflows_to_run is None:
        workflows_to_run = ["W1", "W5", "W3", "W2", "W4"]
    if models_to_run is None:
        models_to_run = list(MODELS.items())  # [(short, id), ...]
    else:
        models_to_run = [(s, MODELS[s]) for s in models_to_run]

    for wf in workflows_to_run:
        log_event(f"=== Starting {wf} ===")
        for model_short, model_id in models_to_run:
            log_event(f"--- {wf} × {model_short} ({model_id}) ---")
            if wf == "W2":
                run_w2(model_short, model_id)
            else:
                docs = SAMPLES[wf]
                run_workflow_standard(wf, model_short, model_id, docs)

    log_event("All done.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--workflows", nargs="+", default=None)
    p.add_argument("--models", nargs="+", default=None)
    args = p.parse_args()
    main(workflows_to_run=args.workflows, models_to_run=args.models)
