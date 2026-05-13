# W2 — Precedent retrieval prompt

**Workflow class:** Retrieval
**Dominant dimensions:** Evidence traceability (D2), Source discipline (D5), Reviewability (D7)

## System message

```
You are a helpful capital-markets analyst.
```

## User message template

You are a debt capital markets analyst. Below is a corpus of corporate bond prospectuses (each clearly headed by document number and issuer name). Answer the following retrieval query:

QUERY: `{query}`

For each matching document, state:
  (a) the document number and issuer name,
  (b) the specific passage or clause that contains the match (quote a short excerpt or describe its location), and
  (c) any specific values that the query asked for (e.g., percentages, thresholds).

If no documents match, state "NO MATCHES FOUND" and explain briefly why.

**Corpus:** 10 documents — 7 SEC EDGAR Rule 424(b)(5) prospectus supplements (HCA, Netflix, Dell/EMC, Cencora, Agilent, Crown Castle, Labcorp) and 3 synthetic Nordic-style term sheets (Nordhavn Industri AB, Fjordkraft Energi Holding AS, Karelis Real Estate ApS). Each document truncated to ~3,000 tokens at the cover-page and key-terms sections.

Return your answer as a markdown table, sorted by document number.

## The five queries

1. **Q1 — Change-of-control put provisions**
   "Identify every document in the provided corpus that contains a change-of-control put provision. For each match: (a) the put price (e.g., 101% of principal, par), (b) the threshold that triggers the put (e.g., acquisition of >50% voting rights), and (c) the section heading where the clause appears."

2. **Q2 — General basket comparison**
   "Across the three synthetic Nordic term sheets in the corpus (Nordhavn Industri AB, Fjordkraft Energi Holding AS, Karelis Real Estate ApS), identify the size of the 'general basket' within the permitted-debt covenant for each. Convert all values to EUR using SEK/EUR = 11.50. Rank from largest to smallest."

3. **Q3 — REIT classification**
   "Identify any document in this corpus where the issuer is a real estate investment trust (REIT). For each, state the basis for your conclusion (form filed, organisational structure, explicit characterisation in the document)."

4. **Q4 — Optional redemption schedules**
   "Compare the optional redemption schedules of the three synthetic Nordic term sheets. For each: (1) non-call period, (2) call price step-downs year by year, (3) presence of equity claw and its terms, (4) any sustainability-linked or non-standard call structure. Return as a comparison table."

5. **Q5 — Healthcare-sector classification**
   "Which documents in this corpus are filed by issuers in the healthcare sector? Healthcare here means hospital operators, healthcare distributors, pharma, or medical devices for patient care — exclude life-sciences instrument or research-tools companies."
