"""
LLM client wrappers for the four models in Option A:

  - claude-opus-4-7              → raicode (Claude API gateway, OpenAI-compatible)
  - claude-sonnet-4-6            → raicode
  - gpt-5                         → OpenAI via Codex CLI (`codex exec` non-interactive)
  - llama-3.3-70b-versatile      → Groq (OpenAI-compatible)

All clients return raw text completion. Idempotent caching is handled at a
higher level by the runner; this file just makes calls.

Rate-limit handling:
  - Groq: free tier ~30 RPM, ~6,000 TPM. Sleep between calls if needed.
  - Raicode and OpenAI: no client-side throttling, rely on server-side.
"""

import os
import json
import subprocess
import time
import shlex
from typing import Optional

from openai import OpenAI

"""API credentials are read from environment variables.

Set them via a `.env` file in this directory (a `.env.example` template is
included in the repo) or export them in your shell before running the pipeline:

  export RAICODE_KEY="..."
  export GROQ_KEY="..."

GPT-5.5 access uses the OpenAI Codex CLI, which manages its own ChatGPT-account
authentication separately — no API key required here.
"""

# Load .env if present (no extra dependency — minimal hand-rolled parser)
import pathlib
_env_path = pathlib.Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        _line = _line.strip()
        if not _line or _line.startswith("#") or "=" not in _line:
            continue
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

RAICODE_KEY = os.environ.get("RAICODE_KEY", "")
RAICODE_BASE_URL = os.environ.get("RAICODE_BASE_URL", "https://gateway.raicode.no/v1")

GROQ_KEY = os.environ.get("GROQ_KEY", "")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

if not RAICODE_KEY or not GROQ_KEY:
    import sys
    sys.stderr.write(
        "[llm_clients] WARNING: RAICODE_KEY and/or GROQ_KEY are not set. "
        "Calls to those providers will fail. Set them in eval/.env or export "
        "them in your shell. See eval/.env.example for the template.\n"
    )


_raicode = OpenAI(base_url=RAICODE_BASE_URL, api_key=RAICODE_KEY)
_groq = OpenAI(base_url=GROQ_BASE_URL, api_key=GROQ_KEY)


def call_raicode(model: str, prompt: str, system: str = "You are a helpful capital-markets analyst.",
                 max_retries: int = 3) -> str:
    """Call Claude via raicode gateway using the responses API."""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = _raicode.responses.create(
                model=model,
                instructions=system,
                input=prompt,
            )
            return resp.output_text
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"raicode call failed for {model}: {last_err}")


def call_groq(prompt: str, system: str = "You are a helpful capital-markets analyst.",
              model: str = "llama-3.3-70b-versatile",
              max_retries: int = 5) -> str:
    """Call Llama 3.3 70B via Groq (OpenAI-compatible chat completions)."""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = _groq.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=4096,
            )
            return resp.choices[0].message.content
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "rate" in err_str or "429" in err_str:
                # Honor rate limit — back off harder
                wait = 30 * (attempt + 1)
                print(f"  Groq rate limit; sleeping {wait}s")
                time.sleep(wait)
            else:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"groq call failed: {last_err}")


def call_codex_gpt5(prompt: str, system: str = "You are a helpful capital-markets analyst.") -> str:
    """Call GPT-5.5 (default Codex model per config.toml) via Codex CLI non-interactive.

    Codex stdout contains a session header + "codex\\n<answer>\\ntokens used\\n<count>" block.
    We parse out the final answer between the last "codex" marker and "tokens used".
    """
    full = system + "\n\n" + prompt
    proc = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "danger-full-access", "-"],
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
            answer = out[codex_idx + len("codex\n"):token_idx].strip()
            return answer
    return out


def call_model(model_id: str, prompt: str, system: str = "You are a helpful capital-markets analyst.") -> str:
    """Unified entry-point: route to provider based on model_id."""
    if model_id.startswith("claude-"):
        return call_raicode(model_id, prompt, system)
    elif model_id == "gpt-5":
        return call_codex_gpt5(prompt, system)
    elif model_id == "llama-3.3-70b-versatile":
        return call_groq(prompt, system)
    else:
        raise ValueError(f"Unknown model id: {model_id}")


# Convenience constants
MODELS = {
    "opus": "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
    "gpt5": "gpt-5",
    "llama": "llama-3.3-70b-versatile",
}

JUDGE_MODEL = "claude-sonnet-4-6"  # Cheaper, used to score outputs


if __name__ == "__main__":
    # Smoke test each provider
    test_prompt = "What is 2+2? Answer in one word."
    print("Testing raicode (Sonnet 4.6)...")
    try:
        out = call_raicode("claude-sonnet-4-6", test_prompt)
        print(f"  -> {out!r}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\nTesting raicode (Opus 4.7)...")
    try:
        out = call_raicode("claude-opus-4-7", test_prompt)
        print(f"  -> {out!r}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\nTesting Groq (Llama 3.3 70B)...")
    try:
        out = call_groq(test_prompt)
        print(f"  -> {out!r}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\nTesting Codex GPT-5...")
    try:
        out = call_codex_gpt5(test_prompt)
        print(f"  -> {out[:200]!r}")
    except Exception as e:
        print(f"  FAIL: {e}")
