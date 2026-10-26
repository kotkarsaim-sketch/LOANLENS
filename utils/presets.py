"""
utils/presets.py - Curated real-world presets for 1-click live demonstration
Includes realistic market rates for Indian public banks, private banks, and NBFCs.
"""

from typing import Dict, Any, List

PRESETS: Dict[str, Dict[str, Any]] = {
    "home_loan_battle": {
        "title": "🏡 Home Loan Face-off (SBI vs HDFC vs ICICI)",
        "description": "₹50 Lakhs over 20 years. Notice how slight rate and fee variances compound into lakhs over 240 months.",
        "category": "Home Loan",
        "loans": [
            {
                "name": "SBI Regular Home Loan",
                "bank": "State Bank of India (PSU)",
                "principal": 5000000,
                "annual_rate_pct": 8.50,
                "tenure_months": 240,
                "processing_fee_pct": 0.35,
                "processing_fee_flat": 0,
                "documentation_charges": 3000,
                "insurance_charges": 0,
                "badge": "Lowest Rate"
            },
            {
                "name": "HDFC Reach Home Loan",
                "bank": "HDFC Bank (Private)",
                "principal": 5000000,
                "annual_rate_pct": 8.70,
                "tenure_months": 240,
                "processing_fee_pct": 0.50,
                "processing_fee_flat": 0,
                "documentation_charges": 4500,
                "insurance_charges": 0,
                "badge": "Popular Private"
            },
            {
                "name": "ICICI Express Home Loan",
                "bank": "ICICI Bank (Private)",
                "principal": 5000000,
                "annual_rate_pct": 8.85,
                "tenure_months": 240,
                "processing_fee_pct": 0.50,
                "processing_fee_flat": 2500,
                "documentation_charges": 5000,
                "insurance_charges": 0,
                "badge": "Fast Disbursal"
            }
        ]
    },
    "personal_loan_fintech": {
        "title": "💳 Personal Loan: Public vs Private vs Fintech NBFC",
        "description": "₹6 Lakhs over 3 years. Demonstrates hidden fees and the true APR gap between banks and instant digital lenders.",
        "category": "Personal Loan",
        "loans": [
            {
                "name": "Bank of Baroda Yoddha",
                "bank": "Bank of Baroda (PSU)",
                "principal": 600000,
                "annual_rate_pct": 10.45,
                "tenure_months": 36,
                "processing_fee_pct": 1.00,
                "processing_fee_flat": 0,
                "documentation_charges": 1000,
                "insurance_charges": 0,
                "badge": "Low Interest"
            },
            {
                "name": "Axis 24x7 Personal Loan",
                "bank": "Axis Bank (Private)",
                "principal": 600000,
                "annual_rate_pct": 11.25,
                "tenure_months": 36,
                "processing_fee_pct": 1.50,
                "processing_fee_flat": 500,
                "documentation_charges": 1500,
                "insurance_charges": 0,
                "badge": "Convenient"
            },
            {
                "name": "QuickCash Fintech NBFC",
                "bank": "Fintech NBFC App",
                "principal": 600000,
                "annual_rate_pct": 14.75,
                "tenure_months": 36,
                "processing_fee_pct": 2.50,
                "processing_fee_flat": 1000,
                "documentation_charges": 2500,
                "insurance_charges": 3500,
                "badge": "Instant / High APR"
            }
        ]
    },
    "auto_ev_comparison": {
        "title": "🚗 Auto Loan: Green EV Concession vs Standard Petrol Car Loan",
        "description": "₹12 Lakhs over 5 years. Comparing promotional green car loans with traditional automotive financing.",
        "category": "Car Loan",
        "loans": [
            {
                "name": "SBI Green Car Loan (EV)",
                "bank": "SBI Green Mobility",
                "principal": 1200000,
                "annual_rate_pct": 8.65,
                "tenure_months": 60,
                "processing_fee_pct": 0.25,
                "processing_fee_flat": 0,
                "documentation_charges": 1200,
                "insurance_charges": 0,
                "badge": "Green Discount"
            },
            {
                "name": "Kotak Prime Auto Loan",
                "bank": "Kotak Mahindra Prime",
                "principal": 1200000,
                "annual_rate_pct": 9.20,
                "tenure_months": 60,
                "processing_fee_pct": 1.00,
                "processing_fee_flat": 1000,
                "documentation_charges": 3000,
                "insurance_charges": 0,
                "badge": "Standard Car Loan"
            }
        ]
    },
    "education_loan": {
        "title": "🎓 Higher Education Loan (Global Studies)",
        "description": "₹25 Lakhs over 7 years. Evaluating public education schemes versus specialized overseas NBFC funding.",
        "category": "Education Loan",
        "loans": [
            {
                "name": "SBI Global Ed-vantage",
                "bank": "SBI Education Scheme",
                "principal": 2500000,
                "annual_rate_pct": 9.65,
                "tenure_months": 84,
                "processing_fee_pct": 0.00,
                "processing_fee_flat": 10000,
                "documentation_charges": 2000,
                "insurance_charges": 0,
                "badge": "Govt Subsidized"
            },
            {
                "name": "Avanse Overseas Student Loan",
                "bank": "Avanse Financial",
                "principal": 2500000,
                "annual_rate_pct": 11.25,
                "tenure_months": 84,
                "processing_fee_pct": 1.25,
                "processing_fee_flat": 5000,
                "documentation_charges": 4500,
                "insurance_charges": 5000,
                "badge": "Collateral-Free"
            }
        ]
    }
}
