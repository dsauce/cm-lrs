# Cross-judge agreement — four judges

Primary judge: **Claude Sonnet 4.6** (in panel, Anthropic family).

Cross-judges:
- **GPT-5.5** (in panel, OpenAI family)
- **Claude Haiku 4.5** (NOT in panel, Anthropic family)
- **Gemini 2.5 Pro** (NOT in panel, Google family — fully external)

All 104 outputs scored by all four judges.

## Per-cell CM-LRS by four judges

| Workflow | Model | Sonnet | GPT-5.5 | Haiku | Gemini | **4-judge avg** |
|---|---|---:|---:|---:|---:|---:|
| W1 | Opus 4.7 | 4.80 | 4.20 | 4.84 | 4.20 | **4.51** |
| W1 | GPT-5.5 | 4.62 | 4.00 | 4.64 | 3.34 | **4.15** |
| W1 | Sonnet 4.6 | 4.95 | 4.11 | 4.79 | 4.14 | **4.50** |
| W1 | Llama 70B | 4.11 | 3.73 | 4.21 | 3.89 | **3.99** |
| W2 | Opus 4.7 | 4.57 | 3.91 | 4.43 | 4.88 | **4.45** |
| W2 | GPT-5.5 | 4.71 | 4.34 | 4.54 | 4.43 | **4.51** |
| W2 | Sonnet 4.6 | 4.74 | 3.91 | 4.77 | 5.00 | **4.61** |
| W2 | Llama 70B | 2.51 | 2.14 | 3.11 | 2.26 | **2.51** |
| W3 | Opus 4.7 | 4.00 | 3.05 | 3.95 | 5.00 | **4.00** |
| W3 | GPT-5.5 | 4.48 | 4.52 | 4.05 | 0.86 | **3.48** |
| W3 | Sonnet 4.6 | 4.05 | 2.71 | 3.76 | 4.67 | **3.80** |
| W3 | Llama 70B | 2.33 | 2.00 | 1.90 | 3.57 | **2.45** |
| W4 | Opus 4.7 | 4.67 | 3.32 | 4.67 | 4.89 | **4.39** |
| W4 | GPT-5.5 | 4.18 | 4.14 | 4.18 | 4.32 | **4.21** |
| W4 | Sonnet 4.6 | 4.68 | 3.21 | 4.71 | 4.25 | **4.21** |
| W4 | Llama 70B | 3.46 | 2.50 | 3.46 | 2.00 | **2.86** |
| W5 | Opus 4.7 | 4.47 | 3.76 | 4.62 | 3.81 | **4.17** |
| W5 | GPT-5.5 | 4.19 | 3.93 | 4.31 | 3.98 | **4.10** |
| W5 | Sonnet 4.6 | 4.76 | 3.88 | 4.74 | 4.43 | **4.45** |
| W5 | Llama 70B | 3.76 | 3.50 | 4.36 | 4.17 | **3.95** |

## Model means across all workflows

| Model | Sonnet | GPT-5.5 | Haiku | Gemini | **4-judge avg** |
|---|---:|---:|---:|---:|---:|
| Opus 4.7 | 4.50 | 3.65 | 4.50 | 4.56 | **4.30** |
| GPT-5.5 | 4.44 | 4.19 | 4.34 | 3.38 | **4.09** |
| Sonnet 4.6 | 4.64 | 3.57 | 4.55 | 4.50 | **4.31** |
| Llama 70B | 3.24 | 2.77 | 3.41 | 3.18 | **3.15** |

## Ranking by judge

- **Sonnet-judge:** Sonnet 4.6 > Opus 4.7 > GPT-5.5 > Llama 70B
- **GPT-5.5-judge:** GPT-5.5 > Opus 4.7 > Sonnet 4.6 > Llama 70B
- **Haiku-judge:** Sonnet 4.6 > Opus 4.7 > GPT-5.5 > Llama 70B
- **Gemini-judge:** Opus 4.7 > Sonnet 4.6 > GPT-5.5 > Llama 70B
- **4-judge average:** Sonnet 4.6 > Opus 4.7 > GPT-5.5 > Llama 70B

## Pairwise Spearman rho on the 20 per-cell aggregates

|  | Sonnet | GPT-5.5 | Haiku | Gemini |
|---|---:|---:|---:|---:|
| **Sonnet**  | 1.000 | 0.665 | 0.925 | 0.380 |
| **GPT-5.5** | 0.665 | 1.000 | 0.523 | 0.033 |
| **Haiku**   | 0.925 | 0.523 | 1.000 | 0.383 |
| **Gemini**  | 0.380 | 0.033 | 0.383 | 1.000 |

## Pearson r per dimension (raw scores, n=104), all six judge pairs

| Dimension | S-G | S-H | S-Gm | G-H | G-Gm | H-Gm | avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| D1 Factual | 0.655 | 0.727 | 0.490 | 0.576 | 0.373 | 0.444 | **0.544** |
| D2 Evidence | 0.643 | 0.703 | 0.359 | 0.489 | 0.288 | 0.404 | **0.481** |
| D3 Numerical | 0.607 | 0.561 | 0.424 | 0.302 | 0.387 | 0.286 | **0.428** |
| D4 Workflow | 0.735 | 0.610 | 0.381 | 0.562 | 0.432 | 0.278 | **0.500** |
| D5 Discipline | 0.644 | 0.700 | 0.523 | 0.530 | 0.409 | 0.405 | **0.535** |
| D6 Decision | 0.815 | 0.748 | 0.278 | 0.730 | 0.253 | 0.305 | **0.522** |
| D7 Review | 0.629 | 0.638 | 0.357 | 0.509 | 0.254 | 0.396 | **0.464** |

## Robust findings (survive all four judges)

- **Llama 3.3 70B is last under every single judge.** On four-judge averaged scoring, the open-weights gap to the strongest frontier model (Sonnet at 4.31) is 1.16 points; to the weakest (GPT-5.5 at 4.09) is 0.94 points.
- **The three frontier closed-source models sit within a 0.22-point band on four-judge averaged means:** Sonnet 4.6 = 4.31, Opus 4.7 = 4.30, GPT-5.5 = 4.09. The in-cluster ranking is judge-dependent: Sonnet first under Sonnet- and Haiku-judges, GPT-5.5 first under GPT-5.5-judge, Opus first under Gemini-judge. All four judges place Opus first or second. The practical reading: the differences between Anthropic and OpenAI top-tier models are within judge-noise for this workload.
- **D6 Decision Usefulness sits in the top tier of inter-judge agreement and shows the widest cross-model dispersion of any dimension.** Mean Pearson r across the six judge pairs = 0.522 for D6, within 0.022 of the highest-agreement dimensions (D1 Factual Accuracy at 0.544 and D5 Source Discipline at 0.535). The strongest cross-family agreement on any dimension in any pair is Sonnet--GPT-5.5 on D6 at 0.815. Combined with D6's largest cross-model dispersion (a 4.0-point spread on the W3 issuer-profile workflow), this makes D6 the cleanest dimension-level production-readiness signal in the rubric -- not on agreement alone, where it is third by a thin margin.

The in-cluster ranking among the three frontier closed-source models is judge-dependent and should not be over-read. The structural finding - frontier-cluster vs open-weights gap, with D6 as the cleanest separator - is robust to judge choice.

All numeric claims above and in the paper are reproducible from the raw judge JSONLs via `eval/verify_numbers.py`.
