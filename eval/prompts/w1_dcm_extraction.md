# W1 — DCM transaction-terms extraction prompt

**Workflow class:** Extraction
**Dominant dimensions:** Factual accuracy (D1), Numerical consistency (D3), Source discipline (D5)

## System message

```
You are a helpful capital-markets analyst.
```

## User message

You are a debt capital markets analyst. The document below is a bond prospectus or term sheet for a corporate debt issuance. Extract the commercial terms into a structured table covering the following fields. For each field, either state the value or write "NOT STATED" if absent. Where you can, cite the section or paragraph where you found the value.

**Fields to extract:**

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

**Document:**

```
{document text — preprocessed to 6,000-token budget}
```

Return your answer as a markdown table with two columns: Field | Value (with section reference).
