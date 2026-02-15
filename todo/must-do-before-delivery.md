# Must-Do Before Delivery

These items should be addressed before the training begins.

## 1. Add DPDPA 2023 Reference in Session 14 — DONE

**Status:** Completed 2026-02-16

**Changes made:**
- `presentation/session14-ai-safety-guardrails.html` — Added DPDPA to Legal Risk card, added new "Data Protection & AI Compliance" slide with DPDPA/GDPR/CCPA/HIPAA comparison table + practical guardrails (Aadhaar, PAN redaction), updated Session Recap with Compliance item
- `hands-on/session-14/lab02_output_validation.ipynb` — Added Aadhaar and PAN regex patterns to PII detection, added DPDPA context note, updated test cases (6 PII types now)
- `hands-on/session-14/solutions/lab02_output_validation.ipynb` — Matching solution updates
- **Bonus:** Removed `admin@oracle.com` from test case, replaced with `admin@unigps.in`

## 2. Add "Where AI Services Fit" Architecture Diagram — DONE

**Status:** Completed 2026-02-16

**Changes made:**
- `presentation/session4-langchain-fundamentals.html` — Added new slide after LangChain Ecosystem showing Python AI agent service alongside Java/Spring Boot microservices, with REST/gRPC communication diagram. Includes speaker notes: "How many microservices does your team maintain? The AI agent is just one more."

## 3. Verify Groq Free-Tier API Sequences — DONE

**Status:** Completed 2026-02-16

**Findings:**
- `llama-3.3-70b-versatile` — confirmed available on Groq (primary model used in labs)
- `llama-3.1-8b-instant` — confirmed available on Groq (fast/cheap alternative)
- Free tier rate limits have improved: ~1,000 RPM, ~250K TPM (was 30 RPM)
- `langchain-groq` v1.1.2 available on PyPI, compatible with requirements.txt

**Changes made:**
- `.env.example` — Updated rate limit comment
- `CLAUDE.md` — Updated Groq rate limits in 2 places
- `presentation/session4-langchain-fundamentals.html` — Replaced deprecated `mixtral-8x7b-32768` with `llama-3.3-70b-versatile`
- `hands-on/session-5/lab01_groq_setup.ipynb` — Removed mixtral from model suggestions

## Bonus: Removed All "Oracle" References — DONE

**Status:** Completed 2026-02-16

Found and replaced 7 occurrences of "Oracle" (client company name) across 4 lab files:
- `hands-on/session-1/lab02_llm_superpowers.ipynb` — "Oracle" → "UniGPS"
- `hands-on/session-1/solutions/lab02_llm_superpowers.ipynb` — "Oracle" → "UniGPS"
- `hands-on/session-3/lab06_memory.ipynb` — "Oracle" → "UniGPS" (3 occurrences)
- `hands-on/session-3/solutions/lab06_memory.ipynb` — "Oracle" → "UniGPS" (3 occurrences)
