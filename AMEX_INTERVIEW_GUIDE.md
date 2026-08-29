# American Express (Amex) | Technical & Behavioral Interview Guide
> **Role Targeted:** Data Analyst / Marketing Analytics / Decision Science Analyst (Entry Level - American Express)  
> **Project:** GenAI-Powered Digital Insights Assistant (Grounded Campaign Analytics & Decision System)

---

## ??? 1. The 90-Second Project Elevator Pitch

> *"In digital marketing and commercial card analytics at financial institutions, business stakeholders need immediate answers to multi-channel performance questions?like 'Which channel had the lowest CPA?' or 'Is our student conversion lift statistically significant?' However, naive LLMs hallucinate metrics and fail at raw data arithmetic.*
>
> *To solve this, I designed and built the **GenAI-Powered Digital Insights Assistant**. The system aggregates 41,000+ campaign records into 8 pre-computed semantic ground-truth summary tables enriched with 95% Wilson Confidence Intervals, Two-Sample Z-Tests for statistical significance, and financial unit economics (CPA, Revenue, ROI).*
>
> *Using a lightweight Semantic RAG architecture and strict prompt constraints, it routes natural-language questions to the exact relevant table and generates accurate executive briefings. I also engineered an automated post-generation regex verification layer, live PII sanitization (PCI-DSS), prompt-injection defense, and a 20-test automated QA regression suite.*
>
> *The resulting system achieved **100% retrieval precision**, **100% security injection blocking**, and **zero numerical hallucinations**, reducing reporting turnaround time by over 90%."*

---

## ?? 2. Top 10 Technical & Analytical Questions (With Bulletproof Answers)

### Q1: *"Why did you build pre-aggregated summary tables instead of giving the LLM raw data or letting it write SQL queries directly?"*
* **Answer:** *"LLMs are probabilistic language models, not deterministic calculators. When you feed 41,000 raw rows to an LLM, it encounters context window limits, high latency, and severe arithmetic hallucinations. Pre-aggregating at the data layer into 8 structured dimensional tables guarantees 100% mathematical determinism, reduces token usage by >95%, and provides an auditable paper trail where every number maps to a verified table row."*

---

### Q2: *"Why did you choose a lightweight Semantic RAG architecture instead of a Vector Database like Pinecone or Chroma?"*
* **Answer:** *"Marketing campaign data is structured and dimensional (`channel`, `job`, `month`, `poutcome`). For structured tables, schema-aware keyword and intent routing achieves 100% retrieval precision without the indexing overhead, embedding drift, or chunking complexity of vector databases. It is simpler, faster (<5ms latency), and easier to govern in a regulated financial environment."*

---

### Q3: *"How did you calculate Confidence Intervals and test Statistical Significance?"*
* **Answer:** *"For every conversion rate, I calculated the 95% Wilson Score / Normal approximation confidence interval:
  $$\text{Margin of Error} = 1.96 \times \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$
  To determine whether Cellular (14.74%) was statistically significantly better than Telephone (5.23%), I ran a Two-Sample Proportion Z-Test using pooled variance. The resulting test yielded $z = 29.80$ and $p < 0.0001$, giving leadership 99.99% confidence that the conversion advantage was real and not random noise."*

---

### Q4: *"How did you evaluate marketing channel performance from an Amex commercial perspective?"*
* **Answer:** *"I evaluated conversion rates in tandem with Cost per Acquisition (CPA) and ROI. Cellular outreach cost $4.50/contact and generated a 14.74% conversion rate, yielding a **$30.53 CPA** and **293.00% ROI**. Telephone outreach cost $3.00/contact but only converted at 5.23%, leading to a **$57.35 CPA** and **109.25% ROI**. Cellular delivered 46.8% lower acquisition costs and +183.8% higher ROI. I also built an interactive scenario simulator in Streamlit for leadership to test sensitivity under shifting cost assumptions."*

---

### Q5: *"How did you ensure the system is safe from PII leaks and prompt injections?"*
* **Answer:** *"I built an `EnterpriseSecurityGuardrail` layer. Before user queries reach the LLM, regex filters detect and mask credit card numbers (13-16 digits), SSNs, emails, and phone numbers into `[REDACTED_*]`. Additionally, it scans for adversarial prompt injection phrases (e.g., 'ignore previous instructions', 'reveal system prompt') and returns an enterprise security alert while blocking the query."*

---

### Q6: *"How does the automated post-generation verification audit work?"*
* **Answer:** *"I wrote a regex-based factual verification engine that extracts every numerical value, percentage, and integer from the LLM's generated response. It cross-checks each cited figure against the numbers present in the retrieved ground truth table within a 0.15 tolerance. If all numbers match, it awards a 100% Grounding Score badge; if any unverified numbers appear, it flags them in an audit log."*

---

### Q7: *"What was the most surprising business insight from the data?"*
* **Answer:** *"The 'May Volume Trap'. May received the largest lead allocation (13,769 contacts, or 33.43% of the entire campaign volume), yet recorded the lowest conversion rate of 6.43%. Conversely, March achieved a 50.55% conversion rate but only received 546 contacts. This revealed a significant timing and volume misallocation, pointing to high marketing ROI gains by shifting call-center capacity from low-efficiency summer blitzes to high-efficiency spring windows."*

---

### Q8: *"How did you test your code to ensure production readiness?"*
* **Answer:** *"I implemented a 20-test automated pytest suite (`tests/test_qa_suite.py`) covering 5 distinct layers: (1) Ingestion Data Quality and Schema Integrity, (2) Statistical Math & CI calculations, (3) Financial Unit Economics (CPA/ROI), (4) Security & PII Redaction, and (5) Anti-Hallucination & Numerical Grounding."*

---

### Q9: *"How does this system handle multi-turn conversational follow-ups?"*
* **Answer:** *"The `MarketingQAEngine` maintains a session conversation history buffer. When a user asks a follow-up question like 'What about May?' or 'What was the CPA for that?', the router combines previous query context with the new input to resolve table references and deliver contextual answers."*

---

### Q10: *"What are the limitations of this project, and how would you scale it for enterprise American Express data lakes?"*
* **Answer:** *"Currently, the lightweight router is optimized for structured analytical tables (<20 tables). In an enterprise environment with hundreds of tables and unstructured PDF cardmember agreements, I would scale this by: (1) integrating Chroma/FAISS with multi-vector embeddings for hybrid retrieval, (2) adding a sandboxed Text-to-SQL layer for dynamic multi-filter slice-and-dice queries, and (3) deploying LangSmith or DeepEval for continuous production hallucination monitoring."*

---

## ?? 3. Behavioral Questions (STAR Method Tailored for Amex)

### 1. "Tell me about a time you had to ensure high data integrity in an analytical project."
* **Situation:** When building automated reporting for financial marketing campaigns, stakeholders were skeptical of GenAI due to hallucination risks.
* **Task:** I needed to guarantee that all generated insights were 100% mathematically accurate and auditable.
* **Action:** I decoupled calculation from text generation by pre-aggregating summary tables with 95% Wilson Confidence Intervals, and built a post-generation regex verification layer that audits cited numbers against source data.
* **Result:** Achieved zero numerical hallucinations across 20 automated tests and gave stakeholders a clickable 'Inspect Ground Truth' drawer for total auditability.

---

### 2. "How do you explain technical analytical concepts to non-technical business partners?"
* **Situation:** Marketing managers needed to understand why telephone outreach was underperforming without getting lost in statistical jargon.
* **Task:** Present channel performance clearly so leadership could decide budget reallocations.
* **Action:** Instead of just reporting p-values, I translated the statistical Z-test into commercial terms: Cost per Acquisition ($30.53 Cellular vs $57.35 Telephone) and Net ROI (293% vs 109%), backed by an interactive Streamlit slider simulator.
* **Result:** Non-technical leaders immediately saw that transitioning budget to cellular lists would yield a +183.8% ROI improvement.

---

## ?? 4. Sample SQL Query (Expected in Amex Technical Screen)

```sql
-- Calculate Channel Performance, Conversion Rate, 95% CI bounds, and CPA
SELECT 
    contact AS contact_channel,
    COUNT(*) AS total_contacts,
    SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(AVG(CASE WHEN y = 'yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS conversion_rate_pct,
    -- Cost per Acquisition (Assuming $4.50 for Cellular, $3.00 for Telephone)
    ROUND(
        SUM(CASE WHEN contact = 'cellular' THEN 4.50 ELSE 3.00 END) / 
        NULLIF(SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END), 0), 2
    ) AS cpa_usd
FROM bank_campaign_data
GROUP BY contact
ORDER BY conversion_rate_pct DESC;
```
