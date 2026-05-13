#!/bin/bash
# Run once all generation + scoring is complete. Produces final scoring table
# and patches the paper LaTeX.

cd "$(dirname "$0")"
set -e

echo "=== Aggregating scores ==="
python3 aggregate.py

echo ""
echo "=== Patching paper LaTeX ==="
python3 patch_paper.py

echo ""
echo "=== Done. ==="
echo "Final scoring table: $(pwd)/scoring_table.md"
echo "Final scoring JSON:  $(pwd)/scoring_table.json"
echo "Paper:               /mnt/c/Working3/arxiv1/CM_LRS_arXiv_Paper.tex"
