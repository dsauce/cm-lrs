# W3 — Issuer profile synthesis prompt

**Workflow class:** Synthesis
**Dominant dimensions:** Evidence traceability (D2), Workflow completeness (D4), Decision usefulness (D6)

## System message

```
You are a helpful capital-markets analyst.
```

## User message

You are a capital-markets analyst. The document below is an annual report (10-K or 20-F) of a public issuer. Produce a one-page structured profile of the issuer covering:

1. Business model and primary segments (with revenue mix if disclosed)
2. Geographic mix of revenue / customers (with percentages if disclosed)
3. Capital structure (key debt / equity instruments outstanding)
4. Most recent year financial trajectory (revenue, EBITDA or operating income, net income — actual values)
5. Top three risk factors (one sentence each)
6. Any disclosed ESG positioning or sustainability targets

Cite the source section / page for each claim. If you cannot find a value, state "NOT DISCLOSED" — do not invent.

**Document:**

```
{document text — preprocessed to 6,000-token budget}
```

Return as a markdown document with the six headings above.
