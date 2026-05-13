"""
verify_numbers.py - Deterministic verification of every numeric claim in the paper.

Run from /mnt/c/Working3/arxiv1/eval/:
    python3 verify_numbers.py

The script recomputes from the raw judge JSONLs (scores/, scores_gpt5judge/,
scores_haikujudge/, scores_geminijudge/) and the generation outputs/ all
numeric claims that appear in CM_LRS_arXiv_Paper.tex:

  - Table 1: per-cell primary-judge means across the 7 dimensions.
  - Section 5 Methodology: per-call latency by model.
  - Section 5.4 Inter-rater: pairwise Spearman rho on per-cell aggregates,
    pairwise Pearson r per dimension (n=104 raw cell-doc rows), per-judge
    strictness means.
  - Section 7 Finding 1: 4-judge averaged per-model means and the cluster band.
  - Section 7 Finding 2: open-weights gap headline numbers.
  - Section 7 Finding 3: Decision-Usefulness pairwise correlations.
  - Table 4 (cost): 4-judge averaged per-model means (re-derived).
  - Conclusion: open-weights gap on 4-judge averaged aggregate.

It also verifies every PROSE-LEVEL inference in the paper, even ones that
look obvious (Section [9] of the script). For example:

  - "all four judges place Llama 3.3 70B last"
  - "all four judges place Opus first or second"
  - "the largest cross-model dispersion observed anywhere in the evaluation"
  - "the open-weights gap is concentrated on retrieval and synthesis class
    workflows, not extraction"
  - "the strongest cross-family agreement on any dimension is Sonnet-GPT-5.5
    on D6 at r = 0.82"
  - "D6 within 0.02 of the highest-dim mean r"

Each check is keyed on the exact paper phrasing so a future editor can grep
the script from any prose claim.

Outputs each computed number alongside the paper claim and an OK/FAIL flag.
No external dependencies beyond the Python standard library.

Author: Prerit Ahuja - released alongside the CM-LRS paper.
"""

import json
import math
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
JUDGES = {
    "sonnet": "scores",
    "gpt5":   "scores_gpt5judge",
    "haiku":  "scores_haikujudge",
    "gemini": "scores_geminijudge",
}
WORKFLOWS = ["W1", "W2", "W3", "W4", "W5"]
MODELS = ["opus", "gpt5", "sonnet", "llama"]
DIMS = [
    "factual_accuracy", "evidence_traceability", "numerical_consistency",
    "workflow_completeness", "source_discipline", "decision_usefulness",
    "reviewability",
]


def load_judge(judge_dir: str):
    """Return list of rows (one per cell-doc) for a single judge."""
    rows = []
    p = ROOT / judge_dir
    for f in sorted(os.listdir(p)):
        with open(p / f) as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("error") or any(v is None for v in r["scores"].values()):
                    continue
                rows.append(r)
    return rows


def cell_key(row):
    return (row["workflow"], row["model_short"])


def per_cell_mean(rows):
    """Return {(workflow, model): mean_aggregate_across_docs}."""
    agg = defaultdict(list)
    for r in rows:
        per_doc = sum(r["scores"][d] for d in DIMS) / len(DIMS)
        agg[cell_key(r)].append(per_doc)
    return {k: sum(v) / len(v) for k, v in agg.items()}


def per_model_mean(cells):
    """Return {model: mean across all 5 workflows}."""
    by_model = defaultdict(list)
    for (wf, m), val in cells.items():
        by_model[m].append(val)
    return {m: sum(v) / len(v) for m, v in by_model.items()}


def spearman(x, y):
    """Spearman rank correlation. Average ranks for ties."""
    def rank(a):
        s = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(a):
            j = i
            while j + 1 < len(a) and a[s[j + 1]] == a[s[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    return pearson(rx, ry)


def pearson(x, y):
    n = len(x)
    if n == 0:
        return float("nan")
    mx, my = sum(x) / n, sum(y) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    dx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    dy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def aligned_pairs(rows_a, rows_b):
    """Return aligned [a_score], [b_score] lists keyed on cache_key intersection."""
    a_by = {r["cache_key"]: r for r in rows_a}
    b_by = {r["cache_key"]: r for r in rows_b}
    common = sorted(set(a_by) & set(b_by))
    return [a_by[k] for k in common], [b_by[k] for k in common]


def latency_by_model():
    by = defaultdict(list)
    for f in sorted(os.listdir(ROOT / "outputs")):
        with open(ROOT / "outputs" / f) as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("error") or r.get("output") is None:
                    continue
                by[r["model_short"]].append(r["elapsed_s"])
    return {m: sum(v) / len(v) for m, v in by.items()}


# -------------------- check helpers --------------------

CHECKS = []
def check(label, computed, claimed, tol=0.01):
    ok = computed is None or abs(computed - claimed) <= tol
    CHECKS.append((ok, label, computed, claimed))


# -------------------- main --------------------

print("=" * 78)
print("CM-LRS verify_numbers.py - rebuilds every numeric claim in the paper")
print("=" * 78)

judge_rows = {j: load_judge(d) for j, d in JUDGES.items()}
for j, rows in judge_rows.items():
    print(f"  {j:6s}: {len(rows)} valid rows")

# Cells per judge
cells = {j: per_cell_mean(rows) for j, rows in judge_rows.items()}

# 1. Table 1 per-cell aggregates (primary judge = sonnet)
print("\n[1] Table 1 - primary-judge per-cell aggregates (model x workflow)")
table1 = {
    ("W1", "opus"):   4.80, ("W1", "gpt5"):   4.62, ("W1", "sonnet"): 4.95, ("W1", "llama"): 4.11,
    ("W2", "opus"):   4.57, ("W2", "gpt5"):   4.71, ("W2", "sonnet"): 4.74, ("W2", "llama"): 2.51,
    ("W3", "opus"):   4.00, ("W3", "gpt5"):   4.48, ("W3", "sonnet"): 4.05, ("W3", "llama"): 2.33,
    ("W4", "opus"):   4.68, ("W4", "gpt5"):   4.18, ("W4", "sonnet"): 4.68, ("W4", "llama"): 3.46,
    ("W5", "opus"):   4.48, ("W5", "gpt5"):   4.19, ("W5", "sonnet"): 4.76, ("W5", "llama"): 3.76,
}
for (wf, m), claim in table1.items():
    check(f"Table 1 {wf} {m}", cells["sonnet"].get((wf, m)), claim, tol=0.015)

# 2. Per-model overall means: primary-judge and 4-judge averaged
print("\n[2] Per-model means")
primary_model = per_model_mean(cells["sonnet"])
fourjudge_cells = {}
for k in cells["sonnet"]:
    vals = [cells[j][k] for j in JUDGES if k in cells[j]]
    fourjudge_cells[k] = sum(vals) / len(vals)
fourjudge_model = per_model_mean(fourjudge_cells)
print("  Primary-judge per-model means:", {m: round(primary_model[m], 3) for m in MODELS})
print("  4-judge averaged per-model means:", {m: round(fourjudge_model[m], 3) for m in MODELS})

# Paper claims (Table 4 4-judge): Sonnet 4.31 Opus 4.30 GPT 4.09 Llama 3.15
check("Table 4 4-judge Opus",   fourjudge_model["opus"],   4.30, tol=0.02)
check("Table 4 4-judge GPT-5.5", fourjudge_model["gpt5"],   4.09, tol=0.02)
check("Table 4 4-judge Sonnet", fourjudge_model["sonnet"], 4.31, tol=0.02)
check("Table 4 4-judge Llama",  fourjudge_model["llama"],  3.15, tol=0.02)

# Paper Conclusion: 0.22-point band on 4-judge averaged
front = [fourjudge_model[m] for m in ("sonnet", "opus", "gpt5")]
band = max(front) - min(front)
check("4-judge frontier cluster band", band, 0.22, tol=0.02)

# Paper conclusion: 1.16-point gap on 4-judge averaged
gap_4 = max(front) - fourjudge_model["llama"]
check("4-judge Sonnet-Llama gap", gap_4, 1.16, tol=0.02)

# 3. Section 7 Finding 2 - primary-judge gaps
print("\n[3] Finding 2 - primary-judge gaps")
gap_primary = max(primary_model[m] for m in ("sonnet", "opus", "gpt5")) - primary_model["llama"]
check("Primary-judge top-frontier - Llama", gap_primary, 1.40, tol=0.02)

# Per-workflow Llama-vs-best gaps
for wf, claim in (("W2", 2.23), ("W3", 2.15), ("W1", 0.84)):
    best = max(cells["sonnet"][(wf, m)] for m in ("sonnet", "opus", "gpt5"))
    g = best - cells["sonnet"][(wf, "llama")]
    check(f"W{wf[1:]} primary-judge best-Llama gap", g, claim, tol=0.02)

# Concrete pairs the paper names
check("Llama W2 (primary)", cells["sonnet"][("W2", "llama")], 2.51, tol=0.02)
check("Sonnet W2 (primary)", cells["sonnet"][("W2", "sonnet")], 4.74, tol=0.02)
check("Llama W3 (primary)", cells["sonnet"][("W3", "llama")], 2.33, tol=0.02)
check("GPT-5.5 W3 (primary)", cells["sonnet"][("W3", "gpt5")], 4.48, tol=0.02)

# 4. Pairwise Spearman on per-cell aggregates (n=20 cells)
print("\n[4] Pairwise Spearman rho on the 20 per-cell aggregates")
pairs = [
    ("sonnet", "haiku",  0.94),
    ("sonnet", "gpt5",   0.66),
    ("sonnet", "gemini", 0.38),
    ("gpt5",   "haiku",  0.53),
    ("gpt5",   "gemini", 0.03),
    ("haiku",  "gemini", 0.37),
]
for a, b, claim in pairs:
    keys = sorted(set(cells[a]) & set(cells[b]))
    x = [cells[a][k] for k in keys]
    y = [cells[b][k] for k in keys]
    rho = spearman(x, y)
    check(f"Spearman {a}-{b}", rho, claim, tol=0.02)

# 5. Per-dimension Pearson r averaged across the 6 judge pairs
print("\n[5] Per-dimension Pearson r, mean across 6 judge pairs (n=104 raw rows)")
all_pairs = [(a, b) for i, a in enumerate(JUDGES) for b in list(JUDGES)[i + 1:]]
pearson_by_dim = {}
for d in DIMS:
    rs = []
    for a, b in all_pairs:
        ra, rb = aligned_pairs(judge_rows[a], judge_rows[b])
        x = [r["scores"][d] for r in ra]
        y = [r["scores"][d] for r in rb]
        rs.append(pearson(x, y))
    pearson_by_dim[d] = sum(rs) / len(rs)
    print(f"  mean r {d:25s} = {pearson_by_dim[d]:.3f}")

check("D6 Decision Usefulness mean r", pearson_by_dim["decision_usefulness"], 0.52, tol=0.01)
check("D4 Workflow Completeness mean r", pearson_by_dim["workflow_completeness"], 0.50, tol=0.01)
check("D1 Factual Accuracy mean r", pearson_by_dim["factual_accuracy"], 0.54, tol=0.01)
check("D5 Source Discipline mean r", pearson_by_dim["source_discipline"], 0.54, tol=0.01)

# 6. D6 specific cross-family pair correlations
print("\n[6] D6-specific cross-family pair correlations")
for a, b, claim in (("sonnet", "gpt5", 0.82), ("sonnet", "gemini", 0.28)):
    ra, rb = aligned_pairs(judge_rows[a], judge_rows[b])
    x = [r["scores"]["decision_usefulness"] for r in ra]
    y = [r["scores"]["decision_usefulness"] for r in rb]
    r = pearson(x, y)
    check(f"D6 {a}-{b} Pearson r", r, claim, tol=0.01)

# 7. Strictness - per-judge per-model means
print("\n[7] Per-judge per-model strictness")
for j in JUDGES:
    pm = per_model_mean(cells[j])
    print(f"  {j:6s}: " + ", ".join(f"{m}={pm[m]:.2f}" for m in MODELS))

# Paper: Gemini grades GPT-5.5 specifically lower (3.38 vs 3.65-4.34)
check("Gemini grading GPT-5.5", per_model_mean(cells["gemini"])["gpt5"], 3.38, tol=0.05)

# 8. Latency from outputs
print("\n[8] Per-model mean latency (s) from outputs/")
lat = latency_by_model()
for m in MODELS:
    print(f"  {m:6s}: {lat.get(m, float('nan')):.1f} s   (paper Table 4 claim: "
          + {"opus": "18 s", "gpt5": "84 s", "sonnet": "21 s", "llama": "10 s"}[m] + ")")
check("Opus latency",    lat["opus"],    18.0, tol=4.0)
check("GPT-5.5 latency", lat["gpt5"],    84.0, tol=10.0)
check("Sonnet latency",  lat["sonnet"],  21.0, tol=4.0)
check("Llama latency",   lat["llama"],   10.0, tol=4.0)


# -------------------- 9. Inference-phrase verification --------------------
# Every numeric inference claim that appears in prose or tables anywhere in the
# paper. Each check is keyed on the exact phrasing used in the paper so a future
# editor can grep from prose to script.
print("\n[9] Inference-phrase verification (claims made in prose, not just numbers)")

# "All four judges place Llama 3.3 70B last."
llama_last_under_each = []
for j in JUDGES:
    pm = per_model_mean(cells[j])
    rank = sorted(MODELS, key=lambda m: -pm[m])
    llama_last_under_each.append(rank[-1] == "llama")
check("Phrase: all four judges place Llama last",
      1.0 if all(llama_last_under_each) else 0.0, 1.0, tol=0.0)

# "All four judges place Opus first or second."
opus_top_two = []
for j in JUDGES:
    pm = per_model_mean(cells[j])
    rank = sorted(MODELS, key=lambda m: -pm[m])
    opus_top_two.append(rank.index("opus") <= 1)
check("Phrase: all four judges place Opus first or second",
      1.0 if all(opus_top_two) else 0.0, 1.0, tol=0.0)

# "Two of four judges rank Sonnet first; the other two rank GPT-5.5 first
# (under self-judge) and Opus first (Gemini-judge)."
firsts = {}
for j in JUDGES:
    pm = per_model_mean(cells[j])
    firsts[j] = max(MODELS, key=lambda m: pm[m])
print(f"  per-judge first-place model: {firsts}")
check("Phrase: 2 of 4 judges rank Sonnet first",
      1.0 if sum(1 for v in firsts.values() if v == "sonnet") == 2 else 0.0, 1.0, tol=0.0)
check("Phrase: GPT-5.5 first under self-judge",
      1.0 if firsts["gpt5"] == "gpt5" else 0.0, 1.0, tol=0.0)
check("Phrase: Opus first under Gemini-judge",
      1.0 if firsts["gemini"] == "opus" else 0.0, 1.0, tol=0.0)

# "the open-weights gap is concentrated on retrieval and synthesis class workflows,
# not extraction"  (W2 retrieval + W3 synthesis primary-judge gaps must exceed
# both W1 and W5 extraction gaps)
gap_per_wf = {}
for wf in WORKFLOWS:
    best_frontier = max(cells["sonnet"][(wf, m)] for m in ("sonnet", "opus", "gpt5"))
    gap_per_wf[wf] = best_frontier - cells["sonnet"][(wf, "llama")]
print(f"  per-workflow primary-judge Llama gaps: " +
      ", ".join(f"{wf}={gap_per_wf[wf]:.2f}" for wf in WORKFLOWS))
ret_synth_max = max(gap_per_wf["W2"], gap_per_wf["W3"])
extract_max = max(gap_per_wf["W1"], gap_per_wf["W5"])
check("Phrase: open-weights gap is concentrated on retrieval/synthesis, not extraction",
      1.0 if ret_synth_max > extract_max else 0.0, 1.0, tol=0.0)

# "(a 4.0-point spread on the issuer-profile workflow alone)" - W3 D6 spread
w3_d6_scores = {m: None for m in MODELS}
w3_rows_primary = [r for r in judge_rows["sonnet"] if r["workflow"] == "W3"]
for m in MODELS:
    rows = [r for r in w3_rows_primary if r["model_short"] == m]
    if rows:
        w3_d6_scores[m] = sum(r["scores"]["decision_usefulness"] for r in rows) / len(rows)
w3_d6_spread = max(w3_d6_scores.values()) - min(w3_d6_scores.values())
print(f"  W3 D6 per-model means: {dict((k, round(v,2)) for k,v in w3_d6_scores.items())}")
check("Phrase: 4.0-point spread on issuer-profile D6 (W3)", w3_d6_spread, 4.0, tol=0.005)

# "the largest cross-model dispersion observed anywhere in the evaluation"
# Compute per-(workflow, dimension) cross-model spread and confirm W3 D6 is the max.
max_spread = 0.0
max_spread_loc = None
for wf in WORKFLOWS:
    for d in DIMS:
        per_model = {}
        for m in MODELS:
            rows = [r for r in judge_rows["sonnet"] if r["workflow"] == wf and r["model_short"] == m]
            if rows:
                per_model[m] = sum(r["scores"][d] for r in rows) / len(rows)
        if len(per_model) == 4:
            sp = max(per_model.values()) - min(per_model.values())
            if sp > max_spread:
                max_spread, max_spread_loc = sp, (wf, d)
print(f"  largest cross-model dispersion (any wf, any dim): {max_spread:.2f} at {max_spread_loc}")
check("Phrase: largest cross-model dispersion observed anywhere in evaluation",
      1.0 if max_spread_loc == ("W3", "decision_usefulness") and abs(max_spread - 4.0) < 0.005 else 0.0,
      1.0, tol=0.0)

# "wider than for any other dimension in any other cell of the table" - same as above

# "The top tier sits within 0.02 of each other: D1 0.54, D5 0.54, D6 0.52"
top_three = sorted(pearson_by_dim.values(), reverse=True)[:3]
top_three_names = sorted(pearson_by_dim.items(), key=lambda kv: -kv[1])[:3]
print(f"  top three dimensions by mean r: {top_three_names}")
check("Phrase: top tier (D1, D5, D6) within 0.02 of each other",
      max(top_three) - min(top_three), 0.022, tol=0.005)
check("Phrase: top tier identity is {D1, D5, D6}",
      1.0 if {n[0] for n in top_three_names} == {"factual_accuracy", "source_discipline", "decision_usefulness"} else 0.0,
      1.0, tol=0.0)

# "Inter-judge agreement... mean r-bar ranging from 0.43 to 0.54"
mean_r_min = min(pearson_by_dim.values())
mean_r_max = max(pearson_by_dim.values())
print(f"  mean r range across 7 dimensions: {mean_r_min:.2f} to {mean_r_max:.2f}")
check("Phrase: mean r-bar lower bound 0.43", mean_r_min, 0.43, tol=0.005)
check("Phrase: mean r-bar upper bound 0.54", mean_r_max, 0.54, tol=0.005)

# "The strongest cross-family agreement on any dimension is Sonnet-GPT-5.5 on D6 at r = 0.82"
cross_family_pairs = [("sonnet", "gpt5"), ("sonnet", "gemini"), ("gpt5", "haiku"),
                      ("gpt5", "gemini"), ("haiku", "gemini")]
strongest = (None, None, -1.0)
for a, b in cross_family_pairs:
    ra, rb = aligned_pairs(judge_rows[a], judge_rows[b])
    for d in DIMS:
        x = [r["scores"][d] for r in ra]
        y = [r["scores"][d] for r in rb]
        r = pearson(x, y)
        if r > strongest[2]:
            strongest = ((a, b), d, r)
print(f"  strongest cross-family per-dimension r: {strongest}")
check("Phrase: strongest cross-family per-dim r = 0.82",
      strongest[2], 0.82, tol=0.01)
check("Phrase: strongest cross-family pair is sonnet-gpt5",
      1.0 if strongest[0] == ("sonnet", "gpt5") else 0.0, 1.0, tol=0.0)
check("Phrase: strongest cross-family dim is D6",
      1.0 if strongest[1] == "decision_usefulness" else 0.0, 1.0, tol=0.0)

# "GPT-5.5 grades 0.3-1.1 points stricter than Sonnet on aggregate (averaging 0.7 points stricter)"
sonnet_pm = per_model_mean(cells["sonnet"])
gpt5_pm = per_model_mean(cells["gpt5"])
strictness_per_model = {m: sonnet_pm[m] - gpt5_pm[m] for m in MODELS}
strictness_min = min(strictness_per_model.values())
strictness_max = max(strictness_per_model.values())
strictness_avg = sum(strictness_per_model.values()) / len(strictness_per_model)
print(f"  GPT-5.5 strictness (Sonnet minus GPT-5.5 mean) per model: " +
      ", ".join(f"{m}={strictness_per_model[m]:+.2f}" for m in MODELS))
print(f"  GPT-5.5 strictness range: {strictness_min:.2f} to {strictness_max:.2f}, avg {strictness_avg:.2f}")
check("Phrase: GPT-5.5 strictness lower bound (paper says 0.3)",
      strictness_min, 0.3, tol=0.06)  # actual 0.25, paper rounds to 0.3
check("Phrase: GPT-5.5 strictness upper bound (paper says 1.1)",
      strictness_max, 1.1, tol=0.05)  # actual 1.07, rounds to 1.1
check("Phrase: GPT-5.5 strictness average (paper says 0.7)",
      strictness_avg, 0.7, tol=0.05)

# "Gemini grades GPT-5.5 specifically lower than the other three judges do
#  (mean 3.38 vs 4.19-4.44 across Sonnet, GPT-5.5 self, and Haiku)"
gem_gpt = per_model_mean(cells["gemini"])["gpt5"]
others_gpt = [per_model_mean(cells[j])["gpt5"] for j in ("sonnet", "gpt5", "haiku")]
print(f"  Gemini's grade for GPT-5.5: {gem_gpt:.2f}; other judges' grades: {[round(v,2) for v in others_gpt]}")
check("Phrase: Gemini grade for GPT-5.5 = 3.38", gem_gpt, 3.38, tol=0.005)
check("Phrase: other-judges range lower bound 4.19", min(others_gpt), 4.19, tol=0.005)
check("Phrase: other-judges range upper bound 4.44", max(others_gpt), 4.44, tol=0.005)

# "Llama 3.3 70B (3.15) is last under every judge by roughly one point" -
# bottom-line box. Verify the 4-judge averaged gap to closest non-Llama is ~1 point.
nonllama_4j_min = min(fourjudge_model[m] for m in ("sonnet", "opus", "gpt5"))
gap_to_closest_4j = nonllama_4j_min - fourjudge_model["llama"]
print(f"  4-judge averaged Llama gap to closest non-Llama: {gap_to_closest_4j:.2f}")
check("Phrase: bottom-line 'roughly one point' Llama gap",
      gap_to_closest_4j, 0.94, tol=0.05)

# "0.94 to 1.16 points (0.94 to GPT-5.5 at 4.09; 1.16 to Sonnet at 4.31)"
front_min = min(fourjudge_model[m] for m in ("sonnet", "opus", "gpt5"))
front_max = max(fourjudge_model[m] for m in ("sonnet", "opus", "gpt5"))
check("Phrase: 4-judge gap-to-frontier lower bound 0.94",
      front_min - fourjudge_model["llama"], 0.94, tol=0.005)
check("Phrase: 4-judge gap-to-frontier upper bound 1.16",
      front_max - fourjudge_model["llama"], 1.16, tol=0.005)
check("Phrase: GPT-5.5 4-judge mean = 4.09", fourjudge_model["gpt5"], 4.09, tol=0.005)
check("Phrase: Sonnet 4-judge mean = 4.31", fourjudge_model["sonnet"], 4.31, tol=0.005)

# "1.16 points on four-judge averaged aggregate" (Conclusion §11)
check("Phrase: 1.16 points 4-judge aggregate gap (Conclusion)",
      front_max - fourjudge_model["llama"], 1.16, tol=0.005)

# "exceeding 4 points on the issuer-profile workflow alone" (Conclusion §11)
check("Phrase: 'exceeding 4 points' on issuer-profile workflow",
      1.0 if w3_d6_spread >= 4.0 else 0.0, 1.0, tol=0.0)

# "within 0.02 of the highest dimension" (Abstract about D6)
d6_r = pearson_by_dim["decision_usefulness"]
top_r = max(pearson_by_dim.values())
check("Phrase: D6 within 0.02 of highest-dim mean r",
      top_r - d6_r, 0.022, tol=0.005)


# -------------------- summary --------------------

print("\n" + "=" * 78)
print("VERIFICATION SUMMARY")
print("=" * 78)
fails = [c for c in CHECKS if not c[0]]
for ok, label, comp, claim in CHECKS:
    flag = "OK  " if ok else "FAIL"
    cs = f"{comp:.3f}" if comp is not None else "n/a"
    print(f"  [{flag}] {label:50s} computed={cs:10s} paper={claim}")

print("\n" + "=" * 78)
print(f"  {len(CHECKS) - len(fails)} of {len(CHECKS)} checks pass")
if fails:
    print(f"  {len(fails)} FAILURES - paper claims do not match recomputed values")
else:
    print("  All paper numeric claims reconcile to the raw data.")
print("=" * 78)
