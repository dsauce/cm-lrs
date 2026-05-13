# Judge prompt — CM-LRS 7-dimension rubric scorer

**Purpose:** Score an LLM output on the 7 CM-LRS reliability dimensions, 0–5 each. Used in the paper's evaluation pipeline. Judge model: Claude Sonnet 4.6 via raicode.

## System message

```
You are a strict but fair evaluator.
```

## User message template

You are scoring an LLM output against the CM-LRS reliability rubric.

**WORKFLOW DESCRIPTION:**
```
{workflow_description}
```

**SOURCE DOCUMENT (truncated for context):**
```
{document — truncated to ~8,000 chars}
```

**MODEL OUTPUT TO SCORE:**
```
{output — truncated to ~6,000 chars}
```

**CM-LRS RUBRIC:**

The CM-LRS (Capital Markets LLM Reliability Score) rubric assesses an LLM output across 7 dimensions, each scored 0–5:

- 0 = Unusable / fabricated
- 1 = Materially flawed
- 2 = Partially useful but risky
- 3 = Acceptable with review
- 4 = Strong with minor review
- 5 = Production-grade / fully traceable

Dimensions:
1. **Factual Accuracy** — Are the stated facts correct against the source document?
2. **Evidence Traceability** — Are claims linked to specific passages, sections, or page references?
3. **Numerical Consistency** — Are numbers, dates, ratios extracted correctly and internally consistent?
4. **Workflow Completeness** — Did the model complete all the requested fields / steps / questions?
5. **Source Discipline** — Did the model avoid unsupported assumptions, hallucinations, or overreach?
6. **Decision Usefulness** — Is the output practically useful to a banker, analyst or reviewer?
7. **Reviewability** — Can a human reviewer quickly verify the output and the reasoning trail?

Score the model output on each of the 7 dimensions, 0–5. For each dimension, provide a one-sentence justification grounded in the source document or the output itself. Return your answer as STRICT JSON with this schema:

```json
{
  "factual_accuracy": {"score": <int 0-5>, "justification": "<one sentence>"},
  "evidence_traceability": {"score": <int 0-5>, "justification": "<one sentence>"},
  "numerical_consistency": {"score": <int 0-5>, "justification": "<one sentence>"},
  "workflow_completeness": {"score": <int 0-5>, "justification": "<one sentence>"},
  "source_discipline": {"score": <int 0-5>, "justification": "<one sentence>"},
  "decision_usefulness": {"score": <int 0-5>, "justification": "<one sentence>"},
  "reviewability": {"score": <int 0-5>, "justification": "<one sentence>"}
}
```

Do not add any commentary outside the JSON.
