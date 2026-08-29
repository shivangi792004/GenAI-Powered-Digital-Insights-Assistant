"""
src/data_validator.py - Automated Data Quality & Schema Integrity Suite

Role: Senior QA & Data Governance Engineer (Amex Financial Standards)
Purpose:
  1. Validates schema contract and data types during ingestion.
  2. Executes range checks, null value assertions, and logical consistency tests.
  3. Generates a Data Quality Health Scorecard for enterprise compliance.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class MarketingDataValidator:
    """
    Enterprise Data Quality Auditor ensuring statistical robustness and ingestion integrity.
    """

    REQUIRED_COLUMNS = [
        'age', 'job', 'marital', 'education', 'default', 'housing',
        'loan', 'contact', 'month', 'duration', 'campaign', 'pdays',
        'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx',
        'cons.conf.idx', 'euribor3m', 'nr.employed', 'y'
    ]

    @classmethod
    def run_full_data_audit(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Runs end-to-end data quality checks and returns an auditable scorecard.
        """
        checks = []
        
        # 1. Schema Completeness Check
        missing_cols = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        checks.append({
            "check_name": "Schema Completeness",
            "passed": len(missing_cols) == 0,
            "details": f"Missing columns: {missing_cols}" if missing_cols else "All 20 required schema fields present."
        })

        # 2. Missing Value (Null) Check
        null_counts = df[cls.REQUIRED_COLUMNS].isnull().sum().to_dict()
        total_nulls = sum(null_counts.values())
        checks.append({
            "check_name": "Null & Missing Value Assertion",
            "passed": total_nulls == 0,
            "details": f"Total null values found: {total_nulls}"
        })

        # 3. Numeric Range Validation
        age_valid = (df['age'] >= 17).all() and (df['age'] <= 110).all()
        duration_valid = (df['duration'] >= 0).all()
        campaign_valid = (df['campaign'] >= 1).all()

        checks.append({
            "check_name": "Range Validity (Age, Call Duration, Campaign Contacts)",
            "passed": bool(age_valid and duration_valid and campaign_valid),
            "details": f"Age [17-110]: {age_valid}, Duration >= 0: {duration_valid}, Campaign >= 1: {campaign_valid}"
        })

        # 4. Target Variable Binary Check
        unique_targets = set(df['y'].dropna().str.lower().unique())
        target_valid = unique_targets.issubset({'yes', 'no'})
        checks.append({
            "check_name": "Target Variable Integrity ('yes'/'no')",
            "passed": bool(target_valid),
            "details": f"Found target values: {list(unique_targets)}"
        })

        # 5. Volume & Statistical Power Check (Minimum sample size for Amex analytics)
        has_adequate_sample = len(df) >= 1000
        checks.append({
            "check_name": "Statistical Power / Sample Size Check",
            "passed": bool(has_adequate_sample),
            "details": f"Dataset contains {len(df):,} records (Threshold >= 1,000)"
        })

        all_passed = all(c['passed'] for c in checks)
        passed_count = sum(1 for c in checks if c['passed'])
        health_score_pct = round((passed_count / len(checks)) * 100, 1)

        return {
            "is_production_ready": all_passed,
            "data_health_score_pct": health_score_pct,
            "total_records_ingested": len(df),
            "total_checks_evaluated": len(checks),
            "check_results": checks
        }


if __name__ == '__main__':
    from src.data_layer import DEFAULT_DATA_PATH
    raw_df = pd.read_csv(DEFAULT_DATA_PATH, sep=';')
    audit = MarketingDataValidator.run_full_data_audit(raw_df)
    print("=== DATA QUALITY SCORECARD ===")
    print(f"Health Score: {audit['data_health_score_pct']}% | Production Ready: {audit['is_production_ready']}")
    for c in audit['check_results']:
        status = "PASSED" if c['passed'] else "FAILED"
        print(f"[{status}] {c['check_name']}: {c['details']}")
