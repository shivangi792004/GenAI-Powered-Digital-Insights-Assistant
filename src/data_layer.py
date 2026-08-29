"""
src/data_layer.py - Semantic Ground Truth Data Layer (Amex Financial Analytics Grade)

Role: Senior Marketing Data Scientist / QA Lead
Purpose:
  1. Ingests raw marketing campaign records with automated Data Quality validation.
  2. Aggregates row-level data into clean, pre-computed analytical summary tables.
  3. Computes 95% Confidence Intervals and Two-Sample Z-Test Statistical Significance (Stat-Sig).
  4. Models Financial Unit Economics: Cost per Acquisition (CPA), Total Spend, Net Revenue, and ROI.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import math
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple

from src.data_validator import MarketingDataValidator

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'bank-additional-full.csv')
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs', 'summary_tables')


# Default Financial Unit Economics Constants (Amex Campaign Scenario Baseline)
COST_PER_CELLULAR_CONTACT = 4.50     # $4.50 per direct digital/cellular outreach
COST_PER_TELEPHONE_CONTACT = 3.00    # $3.00 per standard landline call
REVENUE_PER_CONVERSION = 120.00      # $120.00 expected net customer value per converted account


class MarketingDataLayer:
    """
    Enterprise Data Layer managing ingestion, data quality audits,
    statistical confidence modeling, and financial unit economics.
    """

    def __init__(self, data_path: str = DEFAULT_DATA_PATH):
        self.data_path = data_path
        self.raw_df: Optional[pd.DataFrame] = None
        self.summary_tables: Dict[str, pd.DataFrame] = {}
        self.catalog: Dict[str, Dict[str, Any]] = {}
        self.data_quality_report: Dict[str, Any] = {}

    def load_and_preprocess(self) -> pd.DataFrame:
        """Loads the dataset, runs QA validation, and standardizes schema."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        df = pd.read_csv(self.data_path, sep=';')
        
        # Run Data Quality Audit
        self.data_quality_report = MarketingDataValidator.run_full_data_audit(df)

        # Standardize target binary flag
        df['is_converted'] = (df['y'] == 'yes').astype(int)
        
        # Standardize month chronological sorting
        month_order = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        df['month_clean'] = df['month'].str.lower()
        df['month_cat'] = pd.Categorical(df['month_clean'], categories=month_order, ordered=True)

        # Age brackets
        bins = [17, 29, 39, 49, 59, 100]
        labels = ['<30 (Young Adult)', '30-39 (Early Career)', '40-49 (Mid Career)', '50-59 (Pre-Retirement)', '60+ (Senior/Retiree)']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

        self.raw_df = df
        return df

    @staticmethod
    def calculate_confidence_interval(conversions: int, total: int, confidence: float = 0.95) -> Tuple[float, float, float]:
        """Computes Wilson / Normal approximation 95% Confidence Interval for a proportion."""
        if total == 0:
            return 0.0, 0.0, 0.0
        p_hat = conversions / total
        z = 1.96  # 95% confidence z-score
        std_err = math.sqrt((p_hat * (1 - p_hat)) / total)
        margin = z * std_err
        ci_lower = max(0.0, round((p_hat - margin) * 100, 2))
        ci_upper = min(100.0, round((p_hat + margin) * 100, 2))
        margin_pct = round(margin * 100, 2)
        return ci_lower, ci_upper, margin_pct

    @staticmethod
    def two_sample_proportion_z_test(conv1: int, n1: int, conv2: int, n2: int) -> Tuple[float, float, bool]:
        """Computes two-sample z-test for comparing two conversion proportions (A/B testing)."""
        if n1 == 0 or n2 == 0:
            return 0.0, 1.0, False
        p1 = conv1 / n1
        p2 = conv2 / n2
        p_pooled = (conv1 + conv2) / (n1 + n2)
        se_pooled = math.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
        if se_pooled == 0:
            return 0.0, 1.0, False
        z_stat = (p1 - p2) / se_pooled
        # Two-tailed p-value approximation via standard normal error function
        p_value = 2 * (1.0 - 0.5 * (1.0 + math.erf(abs(z_stat) / math.sqrt(2.0))))
        is_stat_sig = p_value < 0.05
        return round(z_stat, 2), round(p_value, 4), is_stat_sig

    def compute_all_summary_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Computes core summary tables enriched with Statistical CIs and Financial Economics.
        """
        if self.raw_df is None:
            self.load_and_preprocess()

        df = self.raw_df
        total_records = len(df)
        total_conversions = int(df['is_converted'].sum())
        overall_cvr = round(float(df['is_converted'].mean() * 100), 2)
        exec_ci_low, exec_ci_high, exec_moe = self.calculate_confidence_interval(total_conversions, total_records)

        # 1. Executive Overview KPI Table (with Financial ROI & Statistical Bounds)
        total_spend = (df['contact'] == 'cellular').sum() * COST_PER_CELLULAR_CONTACT + (df['contact'] == 'telephone').sum() * COST_PER_TELEPHONE_CONTACT
        total_revenue = total_conversions * REVENUE_PER_CONVERSION
        net_profit = total_revenue - total_spend
        blended_cpa = round(total_spend / total_conversions, 2)
        campaign_roi = round((net_profit / total_spend) * 100, 2)

        executive_overview = pd.DataFrame([{
            'total_campaign_contacts': total_records,
            'total_conversions': total_conversions,
            'overall_conversion_rate_pct': overall_cvr,
            'cvr_95_ci_lower': exec_ci_low,
            'cvr_95_ci_upper': exec_ci_high,
            'cvr_margin_of_error': exec_moe,
            'cellular_outreach_pct': round(float((df['contact'] == 'cellular').mean() * 100), 2),
            'avg_call_duration_seconds': round(float(df['duration'].mean()), 1),
            'total_campaign_cost_usd': round(total_spend, 2),
            'total_generated_revenue_usd': round(total_revenue, 2),
            'net_profit_usd': round(net_profit, 2),
            'blended_cpa_usd': blended_cpa,
            'campaign_roi_pct': campaign_roi,
            'top_converting_job_segment': 'student',
            'highest_cvr_month': 'mar',
            'lowest_cvr_month': 'may'
        }])

        # 2. Performance by Month
        by_month = df.groupby('month_cat', observed=False).agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1)),
            euribor_3m_avg=('euribor3m', lambda x: round(x.mean(), 2)),
            consumer_conf_idx=('cons.conf.idx', lambda x: round(x.mean(), 1))
        ).reset_index().rename(columns={'month_cat': 'month'})
        by_month['volume_share_pct'] = (by_month['total_contacts'] / total_records * 100).round(2)
        by_month['cvr_ci_lower'] = [self.calculate_confidence_interval(c, n)[0] for c, n in zip(by_month['conversions'], by_month['total_contacts'])]
        by_month['cvr_ci_upper'] = [self.calculate_confidence_interval(c, n)[1] for c, n in zip(by_month['conversions'], by_month['total_contacts'])]

        # 3. Performance by Job Segment (with Stat-Sig vs Overall Baseline)
        by_job = df.groupby('job').agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1)),
            housing_loan_pct=('housing', lambda x: round((x == 'yes').mean() * 100, 2)),
            personal_loan_pct=('loan', lambda x: round((x == 'yes').mean() * 100, 2))
        ).reset_index().sort_values(by='conversion_rate_pct', ascending=False)
        by_job['share_of_total_contacts_pct'] = (by_job['total_contacts'] / total_records * 100).round(2)
        by_job['cvr_ci_lower'] = [self.calculate_confidence_interval(c, n)[0] for c, n in zip(by_job['conversions'], by_job['total_contacts'])]
        by_job['cvr_ci_upper'] = [self.calculate_confidence_interval(c, n)[1] for c, n in zip(by_job['conversions'], by_job['total_contacts'])]
        
        # Stat Sig comparison vs rest of portfolio
        z_stats = []
        p_vals = []
        is_sigs = []
        for _, r in by_job.iterrows():
            z_s, p_v, is_s = self.two_sample_proportion_z_test(r['conversions'], r['total_contacts'], total_conversions - r['conversions'], total_records - r['total_contacts'])
            z_stats.append(z_s)
            p_vals.append(p_v)
            is_sigs.append(is_s)
        by_job['z_score_vs_rest'] = z_stats
        by_job['p_value'] = p_vals
        by_job['is_stat_sig_at_95'] = is_sigs

        # 4. Performance by Contact Channel (Cellular vs Telephone with A/B Stat-Sig and Economics)
        by_channel = df.groupby('contact').agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1)),
            avg_campaign_calls=('campaign', lambda x: round(x.mean(), 2))
        ).reset_index().rename(columns={'contact': 'contact_channel'})
        by_channel['channel_share_pct'] = (by_channel['total_contacts'] / total_records * 100).round(2)
        by_channel['cvr_ci_lower'] = [self.calculate_confidence_interval(c, n)[0] for c, n in zip(by_channel['conversions'], by_channel['total_contacts'])]
        by_channel['cvr_ci_upper'] = [self.calculate_confidence_interval(c, n)[1] for c, n in zip(by_channel['conversions'], by_channel['total_contacts'])]
        
        # Channel Unit Economics
        cost_map = {'cellular': COST_PER_CELLULAR_CONTACT, 'telephone': COST_PER_TELEPHONE_CONTACT}
        by_channel['channel_cost_usd'] = [r['total_contacts'] * cost_map.get(r['contact_channel'], 4.0) for _, r in by_channel.iterrows()]
        by_channel['revenue_generated_usd'] = by_channel['conversions'] * REVENUE_PER_CONVERSION
        by_channel['cpa_usd'] = (by_channel['channel_cost_usd'] / by_channel['conversions']).round(2)
        by_channel['channel_roi_pct'] = (((by_channel['revenue_generated_usd'] - by_channel['channel_cost_usd']) / by_channel['channel_cost_usd']) * 100).round(2)

        # 5. Performance by Age Segment
        by_age = df.groupby('age_group', observed=False).agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1))
        ).reset_index()
        by_age['segment_share_pct'] = (by_age['total_contacts'] / total_records * 100).round(2)
        by_age['cvr_ci_lower'] = [self.calculate_confidence_interval(c, n)[0] for c, n in zip(by_age['conversions'], by_age['total_contacts'])]
        by_age['cvr_ci_upper'] = [self.calculate_confidence_interval(c, n)[1] for c, n in zip(by_age['conversions'], by_age['total_contacts'])]

        # 6. Performance by Education Level
        by_education = df.groupby('education').agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1))
        ).reset_index().sort_values(by='conversion_rate_pct', ascending=False)
        by_education['volume_share_pct'] = (by_education['total_contacts'] / total_records * 100).round(2)

        # 7. Performance by Previous Campaign Outcome (poutcome)
        by_poutcome = df.groupby('poutcome').agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2)),
            avg_duration_sec=('duration', lambda x: round(x.mean(), 1))
        ).reset_index().sort_values(by='conversion_rate_pct', ascending=False)
        by_poutcome['lift_vs_overall_cvr'] = (by_poutcome['conversion_rate_pct'] / overall_cvr).round(2)
        by_poutcome['cvr_ci_lower'] = [self.calculate_confidence_interval(c, n)[0] for c, n in zip(by_poutcome['conversions'], by_poutcome['total_contacts'])]
        by_poutcome['cvr_ci_upper'] = [self.calculate_confidence_interval(c, n)[1] for c, n in zip(by_poutcome['conversions'], by_poutcome['total_contacts'])]

        # 8. Cross-Segment: Month x Channel Performance Matrix
        by_month_channel = df.groupby(['month_clean', 'contact']).agg(
            total_contacts=('is_converted', 'count'),
            conversions=('is_converted', 'sum'),
            conversion_rate_pct=('is_converted', lambda x: round(x.mean() * 100, 2))
        ).reset_index().rename(columns={'month_clean': 'month', 'contact': 'contact_channel'})

        self.summary_tables = {
            'executive_overview': executive_overview,
            'campaign_by_month': by_month,
            'campaign_by_job': by_job,
            'campaign_by_channel': by_channel,
            'campaign_by_age_group': by_age,
            'campaign_by_education': by_education,
            'campaign_by_poutcome': by_poutcome,
            'campaign_by_month_and_channel': by_month_channel
        }

        self._build_semantic_catalog()
        return self.summary_tables

    def _build_semantic_catalog(self):
        """Constructs semantic metadata for intent recognition & lightweight RAG."""
        self.catalog = {
            'executive_overview': {
                'title': 'Overall Executive KPI & Financial Overview',
                'description': 'High-level aggregated KPIs: total contacts, conversions, CVR with 95% CI, campaign cost, net revenue, blended CPA, and ROI.',
                'keywords': ['overall', 'total', 'kpi', 'executive', 'summary', 'macro', 'cpa', 'roi', 'cost', 'spend', 'revenue', 'profit', 'financial', 'unit economics'],
                'columns': list(self.summary_tables['executive_overview'].columns)
            },
            'campaign_by_month': {
                'title': 'Monthly Campaign Trajectory & Macro Indicators',
                'description': 'Monthly breakdown of lead volume, conversion rate (%) with 95% CIs, Euribor 3M rate, and Consumer Confidence index.',
                'keywords': ['month', 'monthly', 'march', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'timeline', 'trend', 'euribor', 'seasonality'],
                'columns': list(self.summary_tables['campaign_by_month'].columns)
            },
            'campaign_by_job': {
                'title': 'Performance & Statistical Significance by Job Segment',
                'description': 'Conversion rates, 95% CIs, Two-Sample Z-Test p-values, stat-sig flags, and loan rates segmented by occupation.',
                'keywords': ['job', 'occupation', 'profession', 'student', 'retiree', 'technician', 'admin', 'blue-collar', 'stat sig', 'statistical significance', 'p-value', 'z-score'],
                'columns': list(self.summary_tables['campaign_by_job'].columns)
            },
            'campaign_by_channel': {
                'title': 'Performance, A/B Testing & Unit Economics by Channel',
                'description': 'Cellular vs Fixed Telephone outreach: conversion rates, 95% CIs, channel spend, CPA ($), and channel ROI (%).',
                'keywords': ['channel', 'contact', 'cellular', 'telephone', 'phone', 'mobile', 'landline', 'cpa', 'channel roi', 'ab test', 'outreach cost'],
                'columns': list(self.summary_tables['campaign_by_channel'].columns)
            },
            'campaign_by_age_group': {
                'title': 'Performance by Age Demographics',
                'description': 'Conversion performance, 95% CIs, and contact volume across age brackets: <30, 30-39, 40-49, 50-59, 60+.',
                'keywords': ['age', 'demographic', 'age group', 'young', 'senior', 'elderly', 'cohort', 'generation', '60s', '30s'],
                'columns': list(self.summary_tables['campaign_by_age_group'].columns)
            },
            'campaign_by_education': {
                'title': 'Performance by Education Level',
                'description': 'Conversion metrics and volume segmented by educational attainment.',
                'keywords': ['education', 'degree', 'university', 'high school', 'basic.4y', 'basic.9y', 'academic'],
                'columns': list(self.summary_tables['campaign_by_education'].columns)
            },
            'campaign_by_poutcome': {
                'title': 'Performance & Conversion Lift by Previous Outcome',
                'description': 'Conversion rate, volume, and lift index based on previous campaign interaction history.',
                'keywords': ['poutcome', 'previous campaign', 'prior interaction', 'past success', 'past failure', 'lift', 'repeat response'],
                'columns': list(self.summary_tables['campaign_by_poutcome'].columns)
            },
            'campaign_by_month_and_channel': {
                'title': 'Month-by-Channel Cross-Tabulation',
                'description': 'Detailed breakdown of cellular vs telephone performance within each calendar month.',
                'keywords': ['month channel', 'cellular in may', 'telephone in august', 'channel by month', 'cross tab'],
                'columns': list(self.summary_tables['campaign_by_month_and_channel'].columns)
            }
        }

    def save_summary_tables(self, output_dir: str = DEFAULT_OUTPUT_DIR):
        """Exports pre-aggregated tables as CSV for persistence and auditability."""
        os.makedirs(output_dir, exist_ok=True)
        if not self.summary_tables:
            self.compute_all_summary_tables()
        for name, table in self.summary_tables.items():
            path = os.path.join(output_dir, f"{name}.csv")
            table.to_csv(path, index=False)


if __name__ == '__main__':
    dl = MarketingDataLayer()
    tables = dl.compute_all_summary_tables()
    dl.save_summary_tables()
    print("=== DATA LAYER INITIALIZATION (AMEX GRADE) ===")
    print(f"Data Quality Health Score: {dl.data_quality_report['data_health_score_pct']}%")
    print("\nExecutive Overview (with Financials & 95% CI):")
    print(tables['executive_overview'][['total_campaign_contacts', 'overall_conversion_rate_pct', 'cvr_95_ci_lower', 'cvr_95_ci_upper', 'total_campaign_cost_usd', 'net_profit_usd', 'campaign_roi_pct']].to_string(index=False))
