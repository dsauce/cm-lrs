"""
Workflow extraction prompts + 7-dimension CM-LRS scoring rubric.

Each workflow has a prompt template that takes the preprocessed document text.
The judge prompt takes (workflow description, document text, model output) and
returns 7 dimension scores.
"""

CM_LRS_RUBRIC = """
The CM-LRS (Capital Markets LLM Reliability Score) rubric assesses an LLM output
across 7 dimensions, each scored 0–5:

0 = Unusable / fabricated
1 = Materially flawed
2 = Partially useful but risky
3 = Acceptable with review
4 = Strong with minor review
5 = Production-grade / fully traceable

Dimensions:
  1. Factual Accuracy        — Are the stated facts correct against the source document?
  2. Evidence Traceability   — Are claims linked to specific passages, sections, or page references?
  3. Numerical Consistency   — Are numbers, dates, ratios extracted correctly and internally consistent?
  4. Workflow Completeness   — Did the model complete all the requested fields / steps / questions?
  5. Source Discipline       — Did the model avoid unsupported assumptions, hallucinations, or overreach?
  6. Decision Usefulness     — Is the output practically useful to a banker, analyst or reviewer?
  7. Reviewability           — Can a human reviewer quickly verify the output and the reasoning trail?
"""

# ---------------- W1: DCM transaction terms extraction ----------------

W1_PROMPT = """You are a debt capital markets analyst. The document below is a bond
prospectus or term sheet for a corporate debt issuance. Extract the commercial
terms into a structured table covering the following fields. For each field,
either state the value or write "NOT STATED" if absent. Where you can, cite the
section or paragraph where you found the value.

Fields to extract:
- Issuer
- Guarantors (if any)
- Instrument type (e.g., Senior Notes, Senior Secured Notes, Subordinated Notes)
- Principal amount (state currency and amount; if multi-tranche, list each tranche)
- Coupon (fixed/floating; if floating, state base rate + margin; if fixed, state rate)
- Tenor / maturity date
- Issue price
- Use of proceeds (one sentence)
- Optional redemption schedule (call dates and call prices, if stated)
- Change-of-control provision (put price; threshold for CoC; if stated)
- Incurrence covenant test (e.g., Net Debt / EBITDA threshold; if stated)
- Restricted payments basket headline
- Negative pledge headline (general carve-out size, if stated)
- Trustee / paying agent
- Listing exchange
- Governing law

Document:
{document}

Return your answer as a markdown table with two columns: Field | Value (with section reference).
"""

# ---------------- W2: Precedent retrieval ----------------
# For W2 the prompt takes a query and a corpus context. We use a simple
# all-docs-in-prompt approach with each doc truncated heavily.

W2_PROMPT = """You are a debt capital markets analyst. Below is a corpus of corporate
bond prospectuses (each clearly headed by document number and issuer name).
Answer the following retrieval query:

QUERY: {query}

For each matching document, state:
  (a) the document number and issuer name,
  (b) the specific passage or clause that contains the match (quote a short excerpt
      or describe its location), and
  (c) any specific values that the query asked for (e.g., percentages, thresholds).

If no documents match, state "NO MATCHES FOUND" and explain briefly why.

Corpus:
{corpus}

Return your answer as a markdown table, sorted by document number.
"""

# ---------------- W3: Issuer profile ----------------

W3_PROMPT = """You are a capital-markets analyst. The document below is an annual
report (10-K or 20-F) of a public issuer. Produce a one-page structured profile
of the issuer covering:

1. Business model and primary segments (with revenue mix if disclosed)
2. Geographic mix of revenue / customers (with percentages if disclosed)
3. Capital structure (key debt / equity instruments outstanding)
4. Most recent year financial trajectory (revenue, EBITDA or operating income, net income — actual values)
5. Top three risk factors (one sentence each)
6. Any disclosed ESG positioning or sustainability targets

Cite the source section / page for each claim. If you cannot find a value, state
"NOT DISCLOSED" — do not invent.

Document:
{document}

Return as a markdown document with the six headings above.
"""

# ---------------- W4: Transaction comparable ----------------

W4_PROMPT = """You are an M&A banker. The document below is a merger proxy or
acquisition announcement for a public M&A transaction. Extract the deal terms
into a structured table covering:

- Target (legal entity)
- Acquirer (legal entity)
- Announcement date
- Closing date (or expected closing)
- Total enterprise value (EV) — if stated
- Equity consideration (cash / stock / mix; per-share value)
- Implied premium to undisturbed share price (if stated)
- Financial advisor to acquirer
- Financial advisor to target
- Legal advisor to target
- Key conditions to closing (top 3)
- Termination fee payable by target (if stated)
- Termination fee payable by acquirer (if stated)

Cite the section / page for each value. If a field is not stated, write "NOT
STATED". Do not invent values.

Document:
{document}

Return as a markdown table with Field | Value | Source columns.
"""

# ---------------- W5: ECM transaction terms ----------------

W5_PROMPT = """You are an equity capital markets analyst. The document below is
an IPO prospectus, follow-on offering prospectus, or convertible note
prospectus. Extract the commercial terms into a structured table covering:

- Issuer
- Instrument type (IPO common stock / follow-on / convertible note / etc.)
- Offering size (state currency; if dual primary + secondary, give both)
- Greenshoe / over-allotment option size (if stated)
- Price range or final price
- Listing exchange and ticker
- Distribution format (e.g., Rule 144A / Regulation S / registered)
- Underwriter syndicate (top 3 names if listed)
- Lock-up period (days, parties bound)
- Use of proceeds (one sentence)
- For convertibles only: coupon, conversion premium, conversion rate, fundamental change mechanism
- Cornerstone investors (if stated, with amount)
- Listing exchange ticker
- Governing law

Cite the section / page for each value. Write "NOT STATED" if absent. Do not invent.

Document:
{document}

Return as a markdown table.
"""

# ---------------- Judge prompt ----------------

JUDGE_PROMPT = """You are scoring an LLM output against the CM-LRS reliability rubric.

WORKFLOW DESCRIPTION:
{workflow_description}

SOURCE DOCUMENT (truncated for context):
{document}

MODEL OUTPUT TO SCORE:
{output}

CM-LRS RUBRIC:
{rubric}

Score the model output on each of the 7 dimensions, 0–5. For each dimension,
provide a one-sentence justification grounded in the source document or the
output itself. Return your answer as STRICT JSON with this schema:

{{
  "factual_accuracy": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "evidence_traceability": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "numerical_consistency": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "workflow_completeness": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "source_discipline": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "decision_usefulness": {{"score": <int 0-5>, "justification": "<one sentence>"}},
  "reviewability": {{"score": <int 0-5>, "justification": "<one sentence>"}}
}}

Do not add any commentary outside the JSON.
"""

WORKFLOW_DESCRIPTIONS = {
    "W1": "Debt-terms extraction: extract structured commercial terms from a corporate bond prospectus.",
    "W2": "Precedent retrieval: identify documents in a corpus that match a banker's clause-level retrieval query.",
    "W3": "Issuer profile: synthesise a one-page issuer profile from a 10-K / 20-F annual report.",
    "W4": "Transaction comparable: extract deal terms from an M&A merger proxy or acquisition announcement.",
    "W5": "ECM transaction terms: extract structured commercial terms from an IPO / follow-on / convertible prospectus.",
}

PROMPTS = {
    "W1": W1_PROMPT,
    "W3": W3_PROMPT,
    "W4": W4_PROMPT,
    "W5": W5_PROMPT,
    # W2 handled separately (multi-doc)
}
