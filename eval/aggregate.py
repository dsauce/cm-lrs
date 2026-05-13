"""
Aggregate per-document scores into the 5x4 scoring table that the paper §7
needs.

Reads /eval/scores/<workflow>_<model>.jsonl
Writes:
  - /eval/scoring_table.md  (markdown report)
  - /eval/scoring_table.json (raw aggregates)
"""

import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/mnt/c/Working3/arxiv1")
SCORES = ROOT / "eval" / "scores"
OUT = ROOT / "eval"

WORKFLOWS = ["W1", "W2", "W3", "W4", "W5"]
MODELS_SHORT = ["opus", "gpt5", "sonnet", "llama"]
MODELS_LABEL = {
    "opus": "Claude Opus 4.7",
    "gpt5": "GPT-5.5",
    "sonnet": "Claude Sonnet 4.6",
    "llama": "Llama 3.3 70B",
}
DIM_KEYS = [
    "factual_accuracy",
    "evidence_traceability",
    "numerical_consistency",
    "workflow_completeness",
    "source_discipline",
    "decision_usefulness",
    "reviewability",
]
DIM_LABELS = {
    "factual_accuracy": "Factual",
    "evidence_traceability": "Evidence",
    "numerical_consistency": "Numerical",
    "workflow_completeness": "Workflow",
    "source_discipline": "Discipline",
    "decision_usefulness": "Decision",
    "reviewability": "Review",
}

# Equal weights — paper §5.3 says equal weights as a baseline; weighted scheme
# discussed but kept equal for the headline table
WEIGHTS = {k: 1.0 / len(DIM_KEYS) for k in DIM_KEYS}


def main():
    # Load every score file
    by_cell = defaultdict(list)  # (workflow, model_short) -> [score_rows]
    for path in sorted(SCORES.glob("*_*.jsonl")):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                wf = row["workflow"]
                m = row["model_short"]
                by_cell[(wf, m)].append(row)

    # Compute aggregates
    aggregates = {}
    for (wf, m), rows in by_cell.items():
        # Per-dimension averages
        dim_avgs = {}
        for d in DIM_KEYS:
            vals = [r["scores"].get(d) for r in rows if r["scores"].get(d) is not None]
            dim_avgs[d] = (sum(vals) / len(vals)) if vals else None
        # CM-LRS weighted aggregate
        valid_dims = [d for d in DIM_KEYS if dim_avgs[d] is not None]
        if valid_dims:
            cm_lrs = sum(WEIGHTS[d] * dim_avgs[d] for d in valid_dims) / sum(WEIGHTS[d] for d in valid_dims)
        else:
            cm_lrs = None
        aggregates[(wf, m)] = {
            "n_docs": len(rows),
            "dim_avgs": dim_avgs,
            "cm_lrs": cm_lrs,
        }

    # Write JSON
    json_out = {f"{wf}|{m}": v for (wf, m), v in aggregates.items()}
    with open(OUT / "scoring_table.json", "w", encoding="utf-8") as f:
        json.dump(json_out, f, indent=2, default=str)

    # Write Markdown headline table (workflow × model, CM-LRS)
    lines = []
    lines.append("# CM-LRS Scoring Table")
    lines.append("")
    lines.append(f"Generated from per-document judge scores. Equal weighting across 7 dimensions.")
    lines.append("")
    lines.append("## Headline table — CM-LRS aggregate (0–5 scale)")
    lines.append("")
    header = "| Workflow | " + " | ".join(MODELS_LABEL[m] for m in MODELS_SHORT) + " |"
    sep = "|---|" + "|".join(["---:" for _ in MODELS_SHORT]) + "|"
    lines.append(header)
    lines.append(sep)
    for wf in WORKFLOWS:
        cells = []
        for m in MODELS_SHORT:
            agg = aggregates.get((wf, m))
            if agg and agg["cm_lrs"] is not None:
                cells.append(f"{agg['cm_lrs']:.2f}")
            else:
                cells.append("—")
        lines.append(f"| **{wf}** | " + " | ".join(cells) + " |")

    # Average row
    avg_row_cells = []
    for m in MODELS_SHORT:
        vals = [aggregates[(wf, m)]["cm_lrs"] for wf in WORKFLOWS
                if (wf, m) in aggregates and aggregates[(wf, m)]["cm_lrs"] is not None]
        avg_row_cells.append(f"{sum(vals)/len(vals):.2f}" if vals else "—")
    lines.append(f"| **Mean** | " + " | ".join(avg_row_cells) + " |")
    lines.append("")

    # Per-workflow dimension breakdown
    lines.append("## Per-workflow dimension breakdown")
    lines.append("")
    for wf in WORKFLOWS:
        lines.append(f"### {wf}")
        lines.append("")
        header = "| Dimension | " + " | ".join(MODELS_LABEL[m] for m in MODELS_SHORT) + " |"
        sep = "|---|" + "|".join(["---:" for _ in MODELS_SHORT]) + "|"
        lines.append(header)
        lines.append(sep)
        for d in DIM_KEYS:
            cells = []
            for m in MODELS_SHORT:
                agg = aggregates.get((wf, m))
                if agg and agg["dim_avgs"].get(d) is not None:
                    cells.append(f"{agg['dim_avgs'][d]:.2f}")
                else:
                    cells.append("—")
            lines.append(f"| {DIM_LABELS[d]} | " + " | ".join(cells) + " |")
        n_row = " | ".join(
            str(aggregates[(wf, m)]["n_docs"]) if (wf, m) in aggregates else "0"
            for m in MODELS_SHORT
        )
        lines.append(f"| _n (docs)_ | {n_row} |")
        lines.append("")

    # Coverage check
    lines.append("## Coverage check")
    lines.append("")
    lines.append("Cells with at least one scored document:")
    lines.append("")
    for wf in WORKFLOWS:
        cells = []
        for m in MODELS_SHORT:
            agg = aggregates.get((wf, m))
            cells.append(f"{m}={agg['n_docs'] if agg else 0}")
        lines.append(f"- **{wf}**: " + ", ".join(cells))

    OUT.joinpath("scoring_table.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote scoring_table.md and scoring_table.json")
    # Print headline to stdout
    for line in lines[:30]:
        print(line)


if __name__ == "__main__":
    main()
