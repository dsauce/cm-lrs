"""
LLM-judge scorer.

For each generation in outputs/<workflow>_<model>.jsonl, call Claude Sonnet
(via raicode) to score the output against the 7-dimension CM-LRS rubric.
Writes scores to scores/<workflow>_<model>.jsonl.

Idempotent: skips scores that already exist for a given (cache_key).
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from llm_clients import call_raicode, JUDGE_MODEL
from prompts import JUDGE_PROMPT, CM_LRS_RUBRIC, WORKFLOW_DESCRIPTIONS

ROOT = Path("/mnt/c/Working3/arxiv1")
OUTPUTS = ROOT / "eval" / "outputs"
SCORES = ROOT / "eval" / "scores"
PREPROC = ROOT / "eval" / "preprocessed"
LOGS = ROOT / "eval" / "logs"
SCORES.mkdir(parents=True, exist_ok=True)

DIM_KEYS = [
    "factual_accuracy",
    "evidence_traceability",
    "numerical_consistency",
    "workflow_completeness",
    "source_discipline",
    "decision_usefulness",
    "reviewability",
]


def log_event(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOGS / "scorer.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def parse_judge_json(text: str) -> dict:
    """Extract JSON object from judge model output. Be lenient about wrapping."""
    # Try direct JSON parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Strip leading/trailing code fences and whitespace
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    # Find first { ... last } in cleaned text
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        chunk = cleaned[start:end + 1]
        try:
            return json.loads(chunk)
        except Exception:
            pass
    # Last resort: try to find a JSON object using regex (matches brace-balanced object)
    m = re.search(r"\{(?:[^{}]|\{[^{}]*\})*\}", cleaned, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    raise ValueError(f"Could not parse judge JSON from: {text[:400]}")


def read_w2_corpus_for_judge() -> str:
    """For W2 judging, pass the actual corpus content (truncated per doc) so
    the judge can verify quoted clauses and basket values against the source.
    The corpus is the same one the runner showed to the models."""
    from runner import W2_CORPUS_KEYS
    parts = []
    for i, k in enumerate(W2_CORPUS_KEYS, 1):
        path = PREPROC / "W1" / f"{k}.txt"
        if not path.exists():
            path = PREPROC / "W2" / f"{k}.txt"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")[:8000]  # ~2K tokens per doc
        parts.append(f"\n=== DOC {i:02d} | {k} ===\n{text}")
    return "".join(parts)


def score_one(gen_row: dict, scores_done: set, out_path: Path) -> dict:
    """Score one generation row. Append to JSONL."""
    cache_key = gen_row["cache_key"]
    if cache_key in scores_done:
        return None
    if gen_row.get("output") is None or gen_row.get("error"):
        # Failed generation — record null scores
        row = {
            "cache_key": cache_key,
            "workflow": gen_row["workflow"],
            "model_short": gen_row["model_short"],
            "doc_key": gen_row["doc_key"],
            "scores": {k: None for k in DIM_KEYS},
            "average": None,
            "error": "generation failed: " + str(gen_row.get("error", ""))[:200],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return row

    # Build judge prompt
    workflow = gen_row["workflow"]
    doc_key = gen_row["doc_key"]
    output = gen_row["output"]

    if workflow == "W2":
        # For W2 we don't pass the full corpus to the judge — pass a summary
        document = read_w2_corpus_for_judge()
        # And include the query as part of workflow description
        from runner import W2_QUERIES
        wf_desc = WORKFLOW_DESCRIPTIONS["W2"] + "\nThe specific query for this output was: " + W2_QUERIES.get(doc_key, doc_key)
    else:
        # Source document is in preprocessed/<workflow>/<doc_key>.txt
        path = PREPROC / workflow / f"{doc_key}.txt"
        if not path.exists():
            # Fall back to W1's preprocessed for synthetics
            path = PREPROC / "W1" / f"{doc_key}.txt"
        if not path.exists():
            log_event(f"WARN source missing for {workflow}/{doc_key}")
            document = "[SOURCE DOCUMENT NOT FOUND]"
        else:
            document = path.read_text(encoding="utf-8")[:8000]  # Truncate to keep judge prompt small
        wf_desc = WORKFLOW_DESCRIPTIONS.get(workflow, workflow)

    prompt = JUDGE_PROMPT.format(
        workflow_description=wf_desc,
        document=document,
        output=output[:6000],  # Truncate model output for judge context
        rubric=CM_LRS_RUBRIC,
    )

    t0 = time.time()
    try:
        judge_text = call_raicode(JUDGE_MODEL, prompt, system="You are a strict but fair evaluator.")
        scores_obj = parse_judge_json(judge_text)
        # Normalise: each dim has {"score": int, "justification": str}
        scores = {}
        justifications = {}
        for dim in DIM_KEYS:
            if dim in scores_obj:
                val = scores_obj[dim]
                if isinstance(val, dict):
                    scores[dim] = int(val.get("score", 0))
                    justifications[dim] = val.get("justification", "")[:300]
                else:
                    scores[dim] = int(val)
                    justifications[dim] = ""
            else:
                scores[dim] = None
                justifications[dim] = "not returned by judge"
        valid_scores = [s for s in scores.values() if s is not None]
        avg = sum(valid_scores) / len(valid_scores) if valid_scores else None
        elapsed = time.time() - t0
        row = {
            "cache_key": cache_key,
            "workflow": workflow,
            "model_short": gen_row["model_short"],
            "doc_key": doc_key,
            "scores": scores,
            "justifications": justifications,
            "average": round(avg, 2) if avg is not None else None,
            "judge_elapsed_s": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "error": None,
        }
    except Exception as e:
        elapsed = time.time() - t0
        row = {
            "cache_key": cache_key,
            "workflow": workflow,
            "model_short": gen_row["model_short"],
            "doc_key": doc_key,
            "scores": {k: None for k in DIM_KEYS},
            "average": None,
            "judge_elapsed_s": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "error": str(e)[:300],
        }

    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return row


def main():
    # Iterate all output files
    for gen_file in sorted(OUTPUTS.glob("*_*.jsonl")):
        name = gen_file.stem  # e.g. "W1_sonnet"
        score_file = SCORES / f"{name}.jsonl"
        # Load existing score cache keys
        scores_done = set()
        if score_file.exists():
            with open(score_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        scores_done.add(json.loads(line)["cache_key"])
                    except Exception:
                        continue

        # Iterate generations
        gens = []
        with open(gen_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    gens.append(json.loads(line))
                except Exception:
                    continue

        new = 0
        for gen in gens:
            if gen["cache_key"] in scores_done:
                continue
            row = score_one(gen, scores_done, score_file)
            if row:
                scores_done.add(gen["cache_key"])
                new += 1
                avg = row.get("average")
                err = row.get("error")
                if err:
                    log_event(f"FAIL {gen_file.stem} {gen['doc_key']}: {err[:120]}")
                else:
                    log_event(f"OK   {gen_file.stem} {gen['doc_key']}: avg={avg}")
        if new == 0:
            log_event(f"-- {name}: all {len(gens)} scored already")
        else:
            log_event(f"== {name}: scored {new} new ({len(gens)} total)")


if __name__ == "__main__":
    main()
