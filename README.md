# GenAI-Powered Digital Insights Assistant

An automated reporting system that combines rigorous statistical analysis with LLM-generated natural language insights — built to eliminate manual reporting overhead and arithmetic hallucination risk in AI-generated business reports.

## Overview

Traditional GenAI reporting tools ask the LLM to both compute numbers *and* narrate them — a design that risks hallucinated statistics. This project decouples those two responsibilities: all numerical computation happens in verified Python/Pandas code, while the LLM is used strictly for natural-language generation and Q&A over pre-validated results.

Built and tested on a 41,188-record digital marketing campaign dataset.

## Key Features

- **Hallucination-safe reporting** — Numbers are computed once in Pandas, validated, and passed to the LLM as grounded context. The LLM never generates or infers numeric values on its own.
- **Statistical validation layer** — Channel performance differences are validated using Wilson Score confidence intervals and two-sample z-tests, not just raw percentage comparisons.
- **Schema-aware retrieval for Q&A** — A retrieval layer grounds every natural-language question in verified summary tables, so answers cite real data rather than the model's memory.
- **Automated executive briefings** — A Streamlit decision portal generates full executive-ready reports on demand.
- **Regression-tested accuracy** — A 20-test regression suite cross-checks every LLM-cited figure against the source data to catch drift or hallucination before it reaches a report.

## Key Results

- Measured a statistically significant channel performance gap: **14.74% CVR (cellular)** vs **5.23% CVR (telephone)**, p < 0.0001
- Findings translated into a **46.8% reduction in Cost Per Acquisition (CPA)** through channel-informed targeting
- Cut manual executive-reporting turnaround from **~3 hours to under 5 seconds**
- Achieved **zero arithmetic hallucination** across all validated outputs, verified via the regression suite

## Tech Stack

| Layer | Tools |
|---|---|
| Data processing | Python, Pandas |
| Statistical validation | Wilson Score Intervals, Two-Sample Z-Tests |
| LLM integration | Gemini API / OpenAI API |
| App interface | Streamlit |
| Testing | Custom regression suite (20 test cases) |

## How It Works

1. **Compute** — Raw campaign data is aggregated and validated in Pandas; all metrics (CVR, CPA, confidence intervals) are calculated deterministically.
2. **Ground** — Verified summary tables are indexed by a schema-aware retrieval layer.
3. **Generate** — The LLM receives only grounded, pre-computed context and generates narrative text — never raw numbers from its own knowledge.
4. **Validate** — Every generated figure is cross-checked against source data via the regression suite before being surfaced.
5. **Deliver** — Final insights are rendered as an executive briefing in the Streamlit portal.

## Why This Architecture

LLMs are unreliable at exact arithmetic and prone to confidently stating incorrect numbers. By strictly separating **what is computed** from **what is narrated**, this project ensures every number in a generated report is traceable to source data — a critical requirement for any business-facing automated reporting tool.

## Author

Shivangi Singh
[LinkedIn](https://linkedin.com/in/shivangisingh04/) • [GitHub](https://github.com/shivangi792004)
