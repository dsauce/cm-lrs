"""
Cross-judge scorer using GPT-5.5 (via Codex CLI) as the judge.

Same logic as scorer.py but routes the judge call through Codex with medium
reasoning effort, and writes scores to /eval/scores_gpt5judge/ so the
existing Sonnet-judge scores are preserved.
"""

import os
import sys
import json
import re
import time
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from prompts import JUDGE_PROMPT, CM_LRS_RUBRIC, WORKFLOW_DESCRIPTIONS

ROOT = Path("/mnt/c/Working3/arxiv1")
OUTPUTS = ROOT / "eval" / "outputs"
SCORES = ROOT / "eval" / "scores_gpt5judge"
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


def call_codex_gpt5_medium(prompt: str, system: str = "You are a strict but fair evaluator.") -> str:
    """Call GPT-5.5 via Codex CLI with medium reasoning effort (faster than xhigh)."""
    full = system + "\n\n" + prompt
    proc = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "danger-full-access",
         "-c", "model_reasoning_effort=\"medium\"", "-"],
        input=full,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"codex exec failed (rc={proc.returncode}): {proc.stderr[:500]}")
    out = proc.stdout
    if "codex\n" in out and "tokens used" in out:
        token_idx = out.rfind("tokens used")
        codex_idx = out.rfind("codex\n", 0, token_idx)
        if codex_idx >= 0:
            return out[codex_idx + len("codex\n"):token_idx].strip()
    return out


def log_event(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOGS / "scorer_gpt5.log", "a", encoding="utf-8") as f:
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
            "judge": "gpt5",
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
        judge_text = call_codex_gpt5_medium(prompt)
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
            "judge": "gpt5",
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
            "judge": "gpt5",
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
