# W5 — ECM transaction-terms extraction prompt

**Workflow class:** Extraction (equity side)
**Dominant dimensions:** Numerical consistency (D3), Source discipline (D5), Reviewability (D7)

## System message

```
You are a helpful capital-markets analyst.
```

## User message

You are an equity capital markets analyst. The document below is an IPO prospectus, follow-on offering prospectus, or convertible note prospectus. Extract the commercial terms into a structured table covering:

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

**Document:**

```
{document text — preprocessed to 6,000-token budget}
```

Return as a markdown table.
