# W2 — Retrieval Queries (5)

**Design principle.** Each query is chosen to stress a different combination of the seven CM-LRS dimensions. Where possible, the queries have a knowable ground-truth answer that can be verified against the synthetic term sheets (where the drafter knows exactly what was written) and the EDGAR documents (where the cover page and a finite set of named clauses make verification possible).

| Q | CM-LRS dimensions stressed | Failure mode it surfaces |
|---|---|---|
| Q1 | Factual accuracy · Evidence traceability · Workflow completeness | Missing one or more documents; hallucinating a put price or threshold |
| Q2 | Numerical consistency · Source discipline | Currency confusion (SEK vs EUR); misreading "general basket" vs other basket types |
| Q3 | Source discipline · Auditability | False positive — incorrectly classifying a non-REIT as a REIT |
| Q4 | Decision usefulness · Reviewability · Evidence traceability | Synthesis without source pointers; superficial comparison |
| Q5 | Source discipline · Workflow completeness | Definitional drift — adding documents that don't fit the user-specified scope |

---

## Q1 — Cross-document factual retrieval

**Query as the LLM would receive it:**

> Identify every document in the provided corpus that contains a change-of-control put provision (sometimes called a "change of control offer", "change of control put", or similar). For each matching document, state:
>
> (a) the put price (e.g., 101% of principal, par, etc.);
> (b) the threshold that triggers the put (e.g., acquisition of more than 50% of voting rights); and
> (c) the precise location of the clause (page, section heading, or paragraph identifier).
>
> Present the answer as a table sorted by document name.

**Ground-truth notes for scoring.**

- All three synthetic term sheets contain explicit CoC put provisions at **101%** with a **>50% voting rights** threshold.
- US 424B5 prospectuses overwhelmingly contain a 101% CoC put for senior unsecured notes, typically conditioned on (a) an acquisition triggering a rating downgrade or (b) acquisition of >50% voting rights. The HCA, Netflix, Dell, Broadcom and Cencora prospectuses all contain such clauses in the "Description of Notes" section.
- The LLM should not invent put prices for documents that do not contain a CoC put.

**Scoring dimensions:** primarily factual accuracy (does each cited price/threshold match the document?), evidence traceability (is the location stated?), and workflow completeness (are all matching documents identified?).

---

## Q2 — Numerical consistency across the synthetic term sheets

**Query as the LLM would receive it:**

> Across the three synthetic Nordic term sheets in the corpus (Nordhavn Industri AB, Fjordkraft Energi Holding AS, and Karelis Real Estate ApS), identify the size of the "general basket" within the permitted-debt covenant for each. Convert all values to EUR for comparison using a single agreed FX rate (state your assumption). Rank the three documents from largest to smallest general basket and identify the largest by absolute size after conversion.

**Ground-truth notes for scoring.**

- Nordhavn Industri AB — general basket: **SEK 150m** under permitted debt baskets, plus a SEK 75m negative pledge general basket. The permitted debt basket is the relevant one.
- Fjordkraft Energi Holding AS — general basket: **EUR 75m** under permitted debt; EUR 30m under negative pledge.
- Karelis Real Estate ApS — general basket: **EUR 50m** under permitted debt; EUR 20m under negative pledge.
- At an illustrative SEK/EUR rate of ~11.50, SEK 150m ≈ EUR 13.0m.
- Correct ranking (permitted-debt general basket, largest first): **Fjordkraft (EUR 75m) > Karelis (EUR 50m) > Nordhavn (~EUR 13m)**.

**Scoring dimensions:** numerical consistency (correct values, correct conversion); source discipline (resists conflating "general basket" with the larger acquired-debt or refinancing baskets).

---

## Q3 — REIT classification (false-positive resistance)

**Query as the LLM would receive it:**

> Identify any document in this corpus where the issuer is a real estate investment trust (REIT). For each, state the basis for your conclusion — citing either the form on which the document is filed, the disclosed organisational structure, or an explicit characterisation as a REIT in the document text.

**Ground-truth notes for scoring.**

- Crown Castle Inc. (#17) is the only US REIT in the EDGAR set. It is also widely understood as one (telecom infrastructure REIT).
- The Karelis Real Estate ApS synthetic is a property holding company, **not** a REIT — it is a Danish private limited liability company. The LLM should not incorrectly classify it as a REIT.
- None of the other 28 documents are REITs.

**Failure modes to score:** false-positive on Karelis (treating "real estate" in the name as REIT-equivalent); missing Crown Castle.

**Scoring dimensions:** source discipline (no hallucinated REIT status), auditability (can a reviewer quickly verify each classification), workflow completeness (Crown Castle should be found).

---

## Q4 — Comparative synthesis of optional redemption schedules

**Query as the LLM would receive it:**

> Compare the optional redemption schedules of the three synthetic Nordic term sheets. Specifically:
>
> 1. Identify the non-call period in each document.
> 2. Identify the call price step-downs (year-by-year if applicable).
> 3. Identify which documents include an equity claw and the maximum redemption percentage / price under that claw.
> 4. Identify any sustainability-linked or other non-standard call structure.
> 5. Present a single comparison table.

**Ground-truth notes for scoring.**

- Nordhavn Industri AB — 5-year NC2 with year-by-year step-down 102.375 / 101.188 / par from years 3, 4, 5; equity claw to 35% at 104.75%; standard make-whole pre-NC2.
- Fjordkraft Energi Holding AS — 4-year NC1 with step-down 103.000 / 101.500 / par; **no equity claw** (consistent with senior unsecured structure); sustainability-linked call price increase to 100.500% if Scope 1/2 reduction targets missed.
- Karelis Real Estate ApS — 5-year NC2 with step-down 102.125 / 101.063 / par; equity claw to 40% at 104.25%; tax call.

**Scoring dimensions:** decision usefulness (does the comparison help a reader?); reviewability (can each comparison cell be verified against source); evidence traceability.

---

## Q5 — Definitional discipline: healthcare-sector classification

**Query as the LLM would receive it:**

> Which documents in this corpus are filed by issuers in the healthcare sector? For this query, "healthcare" means hospital operators, healthcare distributors, pharmaceutical companies, or medical-device companies whose primary customers are patient-care settings. Exclude life-sciences instrument or research-tools companies, even if they sell some products into patient-care settings.

**Ground-truth notes for scoring.**

- **In-scope:** HCA Inc. (hospital operator), Cencora Inc. (healthcare distributor — supplies pharmacies and hospitals). Both fit the user-supplied definition.
- **Edge cases requiring judgement:** Labcorp Holdings (clinical-lab diagnostics — primary customers are patient-care settings, so plausibly in-scope); Agilent Technologies (life-sciences instruments — explicitly *excluded* by the user-supplied definition).
- **Out-of-scope:** all other 26 documents.

**Failure modes to score:**

- Adding Agilent (definitional drift — the user explicitly excluded life-sciences instruments).
- Omitting Labcorp without comment (workflow completeness; the question deserves the judgement call to be made explicitly).
- Adding any other document.

**Scoring dimensions:** source discipline (no drift), workflow completeness (handle edge cases), reviewability (explicit reasoning on edge cases).

---

## Notes on scoring rubric integration

Each query produces a per-model output. That output is then scored against the seven CM-LRS dimensions (0–5 each) using the rubric in §5.2 of the paper. Q1 and Q4 will produce the richest scoring discussion because they require both retrieval and synthesis; Q3 and Q5 will be the cleanest indicators of source discipline.

---

*Compiled 2026-05-12.*
