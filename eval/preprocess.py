"""
Preprocess corpus documents: strip HTML to clean text, truncate to a fixed token budget,
cache to /eval/preprocessed/.

Run idempotently — if a preprocessed file already exists, skip.
"""

import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import tiktoken

ROOT = Path("/mnt/c/Working3/arxiv1")
CORPUS = ROOT / "corpus"
OUT = ROOT / "eval" / "preprocessed"
OUT.mkdir(parents=True, exist_ok=True)

# Token budget per document. 6K is generous for Llama 3.3 70B on Groq free tier
# (6000 TPM) and equally fair across all four models since we send the same input.
TOKEN_BUDGET = 6000

ENC = tiktoken.get_encoding("cl100k_base")


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    text = soup.get_text(separator=" ")
    # Normalise whitespace
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"&nbsp;|\xa0", " ", text)
    text = text.strip()
    return text


def truncate(text: str, budget: int = TOKEN_BUDGET) -> str:
    toks = ENC.encode(text)
    if len(toks) <= budget:
        return text
    truncated = ENC.decode(toks[:budget])
    return truncated + "\n\n[...DOCUMENT TRUNCATED TO {} TOKENS FOR EVALUATION...]".format(budget)


def process_file(src: Path, dst: Path) -> dict:
    if dst.exists():
        # Already done
        return {"src": str(src), "status": "cached", "tokens": None}

    raw = src.read_text(encoding="utf-8", errors="ignore")

    if src.suffix == ".md":
        clean = raw  # markdown synthetics are already clean
    else:
        clean = html_to_text(raw)

    truncated = truncate(clean)
    actual_tokens = len(ENC.encode(truncated))

    dst.write_text(truncated, encoding="utf-8")
    return {"src": str(src), "status": "processed", "tokens": actual_tokens}


def walk_workflow(workflow_dir: Path, prefix: str):
    """Process all .htm and .md files under a workflow folder."""
    out_dir = OUT / prefix
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(workflow_dir.rglob("*.htm")):
        # Skip W2 hardlinks (already processed in W1)
        if "W2_precedent_retrieval/edgar" in str(path):
            # Use W1 preprocessed copy if same filename exists
            pass
        out_name = path.stem + ".txt"
        rows.append(process_file(path, out_dir / out_name))
    for path in sorted(workflow_dir.rglob("synthetic/*.md")):
        out_name = "synth_" + path.stem + ".txt"
        rows.append(process_file(path, out_dir / out_name))
    return rows


def main():
    workflows = [
        ("W1", CORPUS / "W1_debt_terms"),
        ("W2", CORPUS / "W2_precedent_retrieval"),
        ("W3", CORPUS / "W3_issuer_profile"),
        ("W4", CORPUS / "W4_transaction_comparable"),
        ("W5", CORPUS / "W5_ecm_terms"),
    ]
    summary = []
    for prefix, src in workflows:
        rows = walk_workflow(src, prefix)
        for r in rows:
            r["workflow"] = prefix
            summary.append(r)
    # Print summary
    processed = sum(1 for r in summary if r["status"] == "processed")
    cached = sum(1 for r in summary if r["status"] == "cached")
    print(f"Processed {processed}, cached {cached}, total {len(summary)}")
    # Per-workflow file counts
    by_wf = {}
    for r in summary:
        by_wf.setdefault(r["workflow"], []).append(r)
    for wf, rows in by_wf.items():
        tokens = [r["tokens"] for r in rows if r["tokens"]]
        avg = sum(tokens) / max(len(tokens), 1)
        print(f"  {wf}: {len(rows)} files, avg {avg:.0f} tokens (cap {TOKEN_BUDGET})")


if __name__ == "__main__":
    main()
