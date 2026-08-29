"""
app.py - GenAI-Powered Digital Insights Assistant (Amex Financial Analytics Grade)

Role: Senior Marketing Data Scientist / QA Lead
Purpose:
  Interactive analytics portal featuring:
  1. Automated Grounded Campaign Briefings with 95% CIs & Financial Unit Economics.
  2. Enterprise Grounded Q&A Assistant with Live PII Redaction & Security Interception.
  3. Interactive Financial ROI & Unit Economics Scenario Simulator.
  4. Statistical Significance (Z-Test) Explorer & Ground Truth Catalog.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import json

from src.data_layer import MarketingDataLayer
from src.insight_generator import GroundedInsightGenerator
from src.qa_engine import MarketingQAEngine
from src.security_guardrails import EnterpriseSecurityGuardrail

# Page Configuration
st.set_page_config(
    page_title="Amex Digital Insights Assistant",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Amex Professional Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #002663;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F0F7FF;
        border: 1px solid #BAE6FD;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-grounded {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 6px 12px;
        border-radius: 16px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-provider {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-sec {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Data Layer
@st.cache_resource
def load_data_layer():
    dl = MarketingDataLayer()
    dl.compute_all_summary_tables()
    return dl

data_layer = load_data_layer()
tables = data_layer.summary_tables
catalog = data_layer.catalog

# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/color/96/american-express.png", width=64)
    st.title("Amex Decision AI")
    st.caption("Grounded Marketing Analytics & Unit Economics Engine")
    
    st.divider()
    st.subheader("?? Model Configuration")
    provider_choice = st.selectbox(
        "AI Generation Provider",
        options=["auto (Recommended)", "gemini", "openai", "offline"],
        index=0,
        help="Select LLM backend or offline deterministic grounded engine."
    )
    provider_val = None if provider_choice.startswith("auto") else provider_choice

    st.divider()
    st.subheader("?? Portfolio Macro KPIs")
    exec_row = tables['executive_overview'].iloc[0]
    st.metric("Total Outreach Leads", f"{int(exec_row['total_campaign_contacts']):,}")
    st.metric("Overall Conversions", f"{int(exec_row['total_conversions']):,}")
    st.metric("Conversion Rate (95% CI)", f"{exec_row['overall_conversion_rate_pct']}%", delta=f"?{exec_row['cvr_margin_of_error']}% MoE")
    st.metric("Net Generated Profit", f"${exec_row['net_profit_usd']:,.2f}", delta=f"{exec_row['campaign_roi_pct']}% ROI")

    st.divider()
    st.success("?? **Enterprise Security Active**: Real-time PII redaction and prompt injection defenses enabled.")

# Header
st.markdown('<div class="main-header">?? American Express | GenAI Digital Insights Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Decision Intelligence, Statistical Significance & Financial Unit Economics</div>', unsafe_allow_html=True)

# Navigation Tabs
tab_briefing, tab_qa, tab_simulator, tab_stats, tab_security = st.tabs([
    "?? Executive Briefing",
    "?? Grounded Marketing Q&A",
    "?? Financial ROI Simulator",
    "?? Statistical & Catalog Explorer",
    "??? Enterprise Security & QA"
])

# ==========================================
# TAB 1: AUTOMATED EXECUTIVE BRIEFING
# ==========================================
with tab_briefing:
    st.subheader("Automated Campaign Executive Briefing")
    st.write("Generates an executive briefing enriched with 95% Confidence Intervals, Two-Sample Z-Test Stat-Sig, and Financial Unit Economics.")

    col_btn, col_badge = st.columns([2, 5])
    with col_btn:
        generate_btn = st.button("?? Generate Executive Briefing", type="primary", use_container_width=True)

    if generate_btn or "briefing_result" in st.session_state:
        if generate_btn:
            with st.spinner("Synthesizing multi-table metrics, calculating confidence intervals, and verifying grounding..."):
                generator = GroundedInsightGenerator(model_provider=provider_val)
                st.session_state["briefing_result"] = generator.generate_campaign_briefing(tables)

        result = st.session_state["briefing_result"]
        verification = result["verification"]

        with col_badge:
            st.markdown(
                f'<span class="badge-grounded">??? Grounding Score: {verification["grounding_score_pct"]}% ({verification["verified_against_ground_truth"]}/{verification["total_numbers_cited"]} numbers verified)</span> '
                f'<span class="badge-provider">Provider: {result["provider"].upper()}</span>',
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown(result["insight_report"])
        
        st.markdown("---")
        st.download_button(
            label="?? Download Executive Briefing (Markdown)",
            data=result["insight_report"],
            file_name="amex_campaign_executive_briefing.md",
            mime="text/markdown"
        )

# ==========================================
# TAB 2: GROUNDED MARKETING Q&A
# ==========================================
with tab_qa:
    st.subheader("Grounded Marketing Analytics Q&A Assistant")
    st.write("Query campaign data in natural language. Queries are routed to verified summary tables, protected by security guardrails, and audited against ground truth.")

    st.markdown("**?? Sample Questions:**")
    sample_queries = [
        "What was the CPA and ROI for cellular vs telephone?",
        "Is the student conversion rate statistically significant compared to other segments?",
        "What was the conversion rate for students vs retirees with 95% confidence intervals?",
        "Which month had the lowest conversion rate and what was its volume?",
        "How does a past successful campaign outcome impact conversion lift?",
        "What was the customer churn rate in 2025?"
    ]
    
    cols = st.columns(3)
    clicked_query = None
    for idx, q in enumerate(sample_queries):
        if cols[idx % 3].button(q, key=f"chip_{idx}", use_container_width=True):
            clicked_query = q

    user_query = st.text_input(
        "Enter your question:",
        value=clicked_query if clicked_query else "",
        placeholder="e.g. What was the Cost per Acquisition (CPA) for cellular outreach?"
    )

    if st.button("?? Submit Question", type="primary") or user_query:
        if user_query.strip():
            with st.spinner("Sanitizing input, routing intent, retrieving ground truth tables, and validating answer..."):
                qa_engine = MarketingQAEngine(data_layer=data_layer, model_provider=provider_val)
                qa_res = qa_engine.answer_question(user_query)

            st.markdown("---")
            st.subheader("?? Grounded Answer")
            st.markdown(qa_res["answer"])

            ver = qa_res["verification"]
            sec = qa_res.get("security_audit", {})
            
            st.markdown(
                f'<div style="margin-top: 15px;">'
                f'<span class="badge-grounded">??? Verified Against: {", ".join(qa_res["retrieved_tables"])} ({ver["grounding_score_pct"]}% Grounding)</span> '
                f'<span class="badge-provider">Engine: {qa_res["provider"].upper()}</span> '
                + (f'<span class="badge-sec">PII Masked: {", ".join(sec.get("detected_pii", []))}</span>' if sec.get("detected_pii") else '') +
                f'</div>',
                unsafe_allow_html=True
            )

            with st.expander("?? View Retrieved Ground Truth Table(s)"):
                for t_name in qa_res["retrieved_tables"]:
                    if t_name in tables:
                        st.markdown(f"**Table: `{t_name}`**")
                        st.dataframe(tables[t_name], use_container_width=True)

# ==========================================
# TAB 3: FINANCIAL ROI SIMULATOR
# ==========================================
with tab_simulator:
    st.subheader("?? Financial Unit Economics & ROI Scenario Simulator")
    st.write("Simulate campaign profitability and CPA under different outreach cost and customer valuation scenarios.")

    col1, col2, col3 = st.columns(3)
    with col1:
        sim_cell_cost = st.slider("Cost per Cellular Contact ($)", min_value=1.0, max_value=15.0, value=4.50, step=0.25)
    with col2:
        sim_tel_cost = st.slider("Cost per Telephone Contact ($)", min_value=1.0, max_value=15.0, value=3.00, step=0.25)
    with col3:
        sim_rev_per_conv = st.slider("Expected Value / Revenue per Conversion ($)", min_value=20.0, max_value=300.0, value=120.00, step=5.0)

    # Dynamic calculation
    raw_df = data_layer.raw_df
    n_cell = int((raw_df['contact'] == 'cellular').sum())
    n_tel = int((raw_df['contact'] == 'telephone').sum())
    conv_cell = int(raw_df[raw_df['contact'] == 'cellular']['is_converted'].sum())
    conv_tel = int(raw_df[raw_df['contact'] == 'telephone']['is_converted'].sum())
    total_conv = conv_cell + conv_tel

    total_cost = (n_cell * sim_cell_cost) + (n_tel * sim_tel_cost)
    total_rev = total_conv * sim_rev_per_conv
    total_profit = total_rev - total_cost
    blended_cpa = total_cost / total_conv if total_conv > 0 else 0
    roi = (total_profit / total_cost * 100) if total_cost > 0 else 0

    st.markdown("### ?? Scenario Financial Impact")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Campaign Spend", f"${total_cost:,.2f}")
    m2.metric("Gross Generated Revenue", f"${total_rev:,.2f}")
    m3.metric("Net Profit", f"${total_profit:,.2f}", delta=f"{roi:.1f}% ROI")
    m4.metric("Blended CPA", f"${blended_cpa:.2f}")

    st.markdown("---")
    st.markdown("#### Channel Comparison Under Current Scenario")
    sim_channel_df = pd.DataFrame([
        {
            "Channel": "Cellular",
            "Contacts": n_cell,
            "Conversions": conv_cell,
            "Conversion Rate (%)": round(conv_cell / n_cell * 100, 2),
            "Spend ($)": round(n_cell * sim_cell_cost, 2),
            "Revenue ($)": round(conv_cell * sim_rev_per_conv, 2),
            "CPA ($)": round((n_cell * sim_cell_cost) / conv_cell, 2),
            "ROI (%)": round(((conv_cell * sim_rev_per_conv - n_cell * sim_cell_cost) / (n_cell * sim_cell_cost)) * 100, 2)
        },
        {
            "Channel": "Telephone",
            "Contacts": n_tel,
            "Conversions": conv_tel,
            "Conversion Rate (%)": round(conv_tel / n_tel * 100, 2),
            "Spend ($)": round(n_tel * sim_tel_cost, 2),
            "Revenue ($)": round(conv_tel * sim_rev_per_conv, 2),
            "CPA ($)": round((n_tel * sim_tel_cost) / conv_tel, 2),
            "ROI (%)": round(((conv_tel * sim_rev_per_conv - n_tel * sim_tel_cost) / (n_tel * sim_tel_cost)) * 100, 2)
        }
    ])
    st.dataframe(sim_channel_df, use_container_width=True)

# ==========================================
# TAB 4: STATISTICAL EXPLORER & CATALOG
# ==========================================
with tab_stats:
    st.subheader("?? Statistical Confidence & Ground Truth Catalog")
    st.write("Inspect all pre-aggregated summary tables, 95% Confidence Intervals, and Two-Sample Z-Test Significance.")

    selected_table_name = st.selectbox(
        "Select Summary Table to Inspect:",
        options=list(tables.keys()),
        format_func=lambda x: f"{catalog[x]['title']} ({x})"
    )

    meta = catalog[selected_table_name]
    st.markdown(f"**Description:** {meta['description']}")
    st.markdown(f"**Keywords:** `{', '.join(meta['keywords'])}`")
    
    st.dataframe(tables[selected_table_name], use_container_width=True)

# ==========================================
# TAB 5: ENTERPRISE SECURITY & QA
# ==========================================
with tab_security:
    st.subheader("??? Enterprise Security, PII Guardrails & QA Health Scorecard")
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown("### ?? Data Quality Audit Report")
        dq = data_layer.data_quality_report
        st.metric("Data Quality Health Score", f"{dq.get('data_health_score_pct', 100.0)}%", delta="Production Ready")
        st.json(dq)

    with col_q2:
        st.markdown("### ?? Live Security & PII Redaction Tester")
        test_sec_input = st.text_area(
            "Test input for PII (Credit Card, SSN, Email) or Prompt Injections:",
            value="Client with card 4532-1234-5678-9010 and email jane@amex.com requested a call."
        )
        if st.button("?? Run Security Inspection"):
            audit_res = EnterpriseSecurityGuardrail.sanitize_and_inspect_input(test_sec_input)
            st.json(audit_res)

st.markdown("---")
st.caption("American Express Marketing Analytics Decision System | 100% Verified Ground Truth & Governance")
