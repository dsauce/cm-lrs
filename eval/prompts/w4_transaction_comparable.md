# W4 — Transaction-comparable reasoning prompt

**Workflow class:** Comparison & Reasoning
**Dominant dimensions:** Numerical consistency (D3), Workflow completeness (D4), Decision usefulness (D6)

## System message

```
You are a helpful capital-markets analyst.
```

## User message

You are an M&A banker. The document below is a merger proxy or acquisition announcement for a public M&A transaction. Extract the deal terms into a structured table covering:

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

Cite the section / page for each value. If a field is not stated, write "NOT STATED". Do not invent values.

**Document:**

```
{document text — preprocessed to 6,000-token budget}
```

Return as a markdown table with Field | Value | Source columns.
