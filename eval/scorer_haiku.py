"""
Third-judge scorer: Claude Haiku 4.5 via raicode.

Haiku 4.5 is NOT in the four-model panel (panel is Opus 4.7, Sonnet 4.6, GPT-5.5,
Llama 3.3 70B), so the self-judge concern is fully eliminated. It is from the
same Anthropic family as the Sonnet judge — family-bias may still apply at the
~5-15% range documented by Zheng et al. 2023 — but self-bias is gone.

Writes scores to /eval/scores_haikujudge/. Idempotent on cache_key.
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from llm_clients import call_raicode
from prompts import JUDGE_PROMPT, CM_LRS_RUBRIC, WORKFLOW_DESCRIPTIONS

ROOT = Path("/mnt/c/Working3/arxiv1")
OUTPUTS = ROOT / "eval" / "outputs"
SCORES = ROOT / "eval" / "scores_haikujudge"
PREPROC = ROOT / "eval" / "preprocessed"
LOGS = ROOT / "eval" / "logs"
SCORES.mkdir(parents=True, exist_ok=True)

HAIKU_MODEL = "claude-haiku-4-5-20251001"

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
    with open(LOGS / "scorer_haiku.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def parse_judge_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        pass
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        chunk = cleaned[start:end + 1]
        try:
            return json.loads(chunk)
        except Exception:
            pass
    m = re.search(r"\{(?:[^{}]|\{[^{}]*\})*\}", cleaned, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    raise ValueError(f"Could not parse judge JSON from: {text[:400]}")


def read_w2_corpus_for_judge() -> str:
    from runner import W2_CORPUS_KEYS
    parts = []
    for i, k in enumerate(W2_CORPUS_KEYS, 1):
        path = PREPROC / "W1" / f"{k}.txt"
        if not path.exists():
            path = PREPROC / "W2" / f"{k}.txt"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")[:8000]
        parts.append(f"\n=== DOC {i:02d} | {k} ===\n{text}")
    return "".join(parts)


def score_one(gen_row: dict, scores_done: set, out_path: Path) -> dict:
    cache_key = gen_row["cache_key"]
    if cache_key in scores_done:
        return None
    if gen_row.get("output") is None or gen_row.get("error"):
        row = {
            "cache_key": cache_key,
            "workflow": gen_row["workflow"],
            "model_short": gen_row["model_short"],
            "doc_key": gen_row["doc_key"],
            "scores": {k: None for k in DIM_KEYS},
            "average": None,
            "error": "generation failed",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "judge": "haiku",
        }
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return row

    workflow = gen_row["workflow"]
    doc_key = gen_row["doc_key"]
    output = gen_row["output"]

    if workflow == "W2":
        document = read_w2_corpus_for_judge()
        from runner import W2_QUERIES
        wf_desc = WORKFLOW_DESCRIPTIONS["W2"] + "\nThe specific query for this output was: " + W2_QUERIES.get(doc_key, doc_key)
    else:
        path = PREPROC / workflow / f"{doc_key}.txt"
        if not path.exists():
            path = PREPROC / "W1" / f"{doc_key}.txt"
        document = path.read_text(encoding="utf-8")[:8000] if path.exists() else "[SOURCE NOT FOUND]"
        wf_desc = WORKFLOW_DESCRIPTIONS.get(workflow, workflow)

    prompt = JUDGE_PROMPT.format(
        workflow_description=wf_desc,
        document=document,
        output=output[:6000],
        rubric=CM_LRS_RUBRIC,
    )

    t0 = time.time()
    try:
        judge_text = call_raicode(HAIKU_MODEL, prompt, system="You are a strict but fair evaluator.")
        scores_obj = parse_judge_json(judge_text)
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
        valid = [s for s in scores.values() if s is not None]
        avg = sum(valid) / len(valid) if valid else None
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
            "judge": "haiku",
            "error": None,
        }
    except Exception as e:
        row = {
            "cache_key": cache_key,
            "workflow": workflow,
            "model_short": gen_row["model_short"],
            "doc_key": doc_key,
            "scores": {k: None for k in DIM_KEYS},
            "average": None,
            "judge_elapsed_s": round(time.time() - t0, 2),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "judge": "haiku",
            "error": str(e)[:300],
        }

    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return row


def main():
    for gen_file in sorted(OUTPUTS.glob("*_*.jsonl")):
        name = gen_file.stem
        score_file = SCORES / f"{name}.jsonl"
        scores_done = set()
        if score_file.exists():
            with open(score_file) as f:
                for line in f:
                    try:
                        scores_done.add(json.loads(line)["cache_key"])
                    except Exception:
                        continue
        gens = []
        with open(gen_file) as f:
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
                if row.get("error"):
                    log_event(f"FAIL {name} {gen['doc_key']}: {row['error'][:120]}")
                else:
                    log_event(f"OK   {name} {gen['doc_key']}: avg={row.get('average')}")
        if new == 0:
            log_event(f"-- {name}: all scored already")
        else:
            log_event(f"== {name}: scored {new} new")


if __name__ == "__main__":
    main()
