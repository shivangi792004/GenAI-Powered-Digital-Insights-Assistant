"""
tests/test_grounding.py - Unit & Grounding Regression Tests

Tests:
  1. Data layer loads and computes summary tables correctly.
  2. Semantic router accurately matches user intent to tables.
  3. Grounding validator correctly flags invalid numbers and approves valid numbers.
  4. Q&A engine produces strictly grounded answers.
"""

import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_layer import MarketingDataLayer
from src.qa_engine import MarketingQAEngine
from src.insight_generator import GroundedInsightGenerator


@pytest.fixture(scope="module")
def data_layer():
    dl = MarketingDataLayer()
    dl.compute_all_summary_tables()
    return dl


def test_data_layer_kpis(data_layer):
    exec_df = data_layer.summary_tables['executive_overview'].iloc[0]
    assert exec_df['total_campaign_contacts'] == 41188
    assert exec_df['total_conversions'] == 4640
    assert exec_df['overall_conversion_rate_pct'] == 11.27
    assert exec_df['top_converting_job_segment'] == 'student'


def test_summary_table_generation(data_layer):
    expected_tables = [
        'executive_overview', 'campaign_by_month', 'campaign_by_job',
        'campaign_by_channel', 'campaign_by_age_group', 'campaign_by_education',
        'campaign_by_poutcome', 'campaign_by_month_and_channel'
    ]
    for table_name in expected_tables:
        assert table_name in data_layer.summary_tables
        assert not data_layer.summary_tables[table_name].empty


def test_semantic_router(data_layer):
    qa = MarketingQAEngine(data_layer=data_layer, model_provider="offline")
    
    # Test Channel routing
    res_chan = qa.retrieve_relevant_tables("How did cellular compare with telephone?")
    assert any(t[0] == 'campaign_by_channel' for t in res_chan)
    
    # Test Job routing
    res_job = qa.retrieve_relevant_tables("Which job segment had the highest conversion rate?")
    assert any(t[0] == 'campaign_by_job' for t in res_job)

    # Test Month routing
    res_mon = qa.retrieve_relevant_tables("What was the conversion rate in March?")
    assert any(t[0] == 'campaign_by_month' for t in res_mon)


def test_grounding_verifier():
    gen = GroundedInsightGenerator()
    ground_truth = [11.27, 41188, 4640, 14.74, 5.23]
    
    # Accurate text
    accurate_text = "Overall conversion was 11.27% across 41,188 contacts. Cellular achieved 14.74%."
    audit = gen.verify_grounding(accurate_text, ground_truth)
    assert audit['is_fully_grounded'] is True
    assert audit['grounding_score_pct'] == 100.0

    # Hallucinated text
    hallucinated_text = "Overall conversion was 99.99% across 80,000 contacts."
    audit_bad = gen.verify_grounding(hallucinated_text, ground_truth)
    assert audit_bad['is_fully_grounded'] is False
    assert 99.99 in audit_bad['unverified_numbers']


def test_offline_qa_grounding(data_layer):
    qa = MarketingQAEngine(data_layer=data_layer, model_provider="offline")
    res = qa.answer_question("How did cellular compare with telephone in conversion rate?")
    assert res['verification']['grounding_score_pct'] == 100.0
    assert "14.74%" in res['answer']
    assert "5.23%" in res['answer']
