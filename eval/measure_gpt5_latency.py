"""
measure_gpt5_latency.py - Direct-API latency measurement for GPT-5.5.

Replaces the Codex CLI 84 s figure in Table 4 with a clean direct-API number
that doesn't include CLI start-up / orchestration overhead.

Usage:
    export OPENAI_API_KEY=sk-...
    python3 measure_gpt5_latency.py [N]

where N is the number of representative cell prompts to time (default 10,
sampled deterministically from the existing W1/W2/W3/W4/W5 generation prompts
already used in this paper).

Cost estimate: ~10 calls x (5K input + 2K output) ~ $0.20-0.40 at 2026 list.

Does NOT modify any scoring data. The existing GPT-5.5 outputs and judge scores
remain unchanged - we are only re-measuring latency, not re-evaluating.
"""

import json
import os
import sys
import time
from pathlib import Path
from urllib import request as urlreq

ROOT = Path(__file__).parent
OUTPUTS = ROOT / "outputs"
PREPROC = ROOT / "preprocessed"

API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not API_KEY:
    print("ERROR: set OPENAI_API_KEY in the environment.")
    print("  export OPENAI_API_KEY=sk-...")
    sys.exit(1)

# The model id Codex CLI was invoking. If a newer string is needed at submission
# time, update this single constant. Reasoning effort is "high" to mirror the
# original generation params.
MODEL_ID = os.environ.get("OPENAI_MODEL_ID", "gpt-5.5")
REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT", "high")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def load_existing_gpt5_calls():
    """Reload the original prompts that were already sent to GPT-5.5 via Codex CLI.
    The outputs/ JSONL stores the input prompt + the response; we replay only the
    prompt to get an apples-to-apples wall-clock comparison."""
    rows = []
    for f in sorted(OUTPUTS.glob("*_gpt5.jsonl")):
        with open(f) as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("error") or r.get("output") is None:
                    continue
                rows.append(r)
    return rows


def reconstruct_prompt(row):
    """Look up the original prompt for this generation row by re-running the
    same prompt-building logic used in runner.py.

    For latency-measurement purposes, we use the document text + the workflow
    prompt template. This recreates the input the model originally received.
    """
    from prompts import (W1_PROMPT, W2_PROMPT, W3_PROMPT, W4_PROMPT, W5_PROMPT,
                         WORKFLOW_DESCRIPTIONS)
    workflow = row["workflow"]
    doc_key = row["doc_key"]
    template = {"W1": W1_PROMPT, "W2": W2_PROMPT, "W3": W3_PROMPT,
                "W4": W4_PROMPT, "W5": W5_PROMPT}[workflow]
    if workflow == "W2":
        from runner import W2_QUERIES, W2_CORPUS_KEYS
        parts = []
        for i, k in enumerate(W2_CORPUS_KEYS, 1):
            path = PREPROC / "W1" / f"{k}.txt"
            if not path.exists():
                path = PREPROC / "W2" / f"{k}.txt"
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")[:8000]
            parts.append(f"\n=== DOC {i:02d} | {k} ===\n{text}")
        document = "".join(parts)
        return template.format(query=W2_QUERIES.get(doc_key, doc_key), document=document)
    else:
        path = PREPROC / workflow / f"{doc_key}.txt"
        if not path.exists():
            path = PREPROC / "W1" / f"{doc_key}.txt"
        document = path.read_text(encoding="utf-8")[:8000] if path.exists() else "[SOURCE NOT FOUND]"
        return template.format(document=document)


def call_openai(prompt: str) -> tuple[float, int]:
    """Direct POST to chat/completions. Returns (wall_clock_s, output_tokens)."""
    body = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "reasoning_effort": REASONING_EFFORT,
    }
    data = json.dumps(body).encode("utf-8")
    req = urlreq.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urlreq.urlopen(req, timeout=600) as resp:
        raw = resp.read().decode("utf-8")
    dt = time.time() - t0
    obj = json.loads(raw)
    out_tokens = obj.get("usage", {}).get("completion_tokens", 0)
    return dt, out_tokens


def main():
    rows = load_existing_gpt5_calls()
    if not rows:
        print("ERROR: no GPT-5.5 outputs found in outputs/ - run generation first")
        sys.exit(2)
    sample = rows[::max(1, len(rows) // N)][:N]
    print(f"Calling {MODEL_ID} (reasoning_effort={REASONING_EFFORT}) on {len(sample)} representative prompts...")
    latencies, output_tokens = [], []
    for r in sample:
        try:
            prompt = reconstruct_prompt(r)
            dt, out_tok = call_openai(prompt)
            latencies.append(dt)
            output_tokens.append(out_tok)
            print(f"  {r['workflow']}/{r['doc_key']:30s}  {dt:6.1f} s   ({out_tok} out tokens)")
        except Exception as e:
            print(f"  {r['workflow']}/{r['doc_key']}  ERROR: {str(e)[:200]}")
    if latencies:
        mean = sum(latencies) / len(latencies)
        print()
        print(f"Direct OpenAI API (no Codex CLI overhead):")
        print(f"  N = {len(latencies)} calls")
        print(f"  mean wall-clock: {mean:.1f} s")
        print(f"  median:          {sorted(latencies)[len(latencies)//2]:.1f} s")
        print(f"  min:             {min(latencies):.1f} s")
        print(f"  max:             {max(latencies):.1f} s")
        print(f"  output tokens:   mean {sum(output_tokens)/len(output_tokens):.0f}")
        print()
        print(f"  Codex CLI baseline (current Table 4): 84 s")
        print(f"  Direct-API delta: {mean - 84:.1f} s ({(mean-84)/84*100:.0f}%)")


if __name__ == "__main__":
    main()
