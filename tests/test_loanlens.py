"""
tests/test_loanlens.py - Test suite for LoanLens financial engine & formatting
"""

import pytest
import pandas as pd
from utils.formatting import format_inr, format_inr_compact, format_percent, format_tenure_display
from utils.financial_engine import (
    calculate_emi,
    solve_apr,
    calculate_loan_summary,
    generate_amortization_schedule,
    generate_annual_schedule,
    simulate_prepayment,
    calculate_affordability,
    find_loan_winner
)
from utils.presets import PRESETS


def test_format_inr():
    assert format_inr(0) == "₹0"
    assert format_inr(500) == "₹500"
    assert format_inr(5000) == "₹5,000"
    assert format_inr(50000) == "₹50,000"
    assert format_inr(500000) == "₹5,00,000"
    assert format_inr(5000000) == "₹50,00,000"
    assert format_inr(12345678) == "₹1,23,45,678"
    assert format_inr(-500000) == "-₹5,00,000"


def test_format_inr_compact():
    assert format_inr_compact(50000000) == "₹5.00 Cr"
    assert format_inr_compact(5000000) == "₹50.00 L"
    assert format_inr_compact(750000) == "₹7.50 L"
    assert format_inr_compact(25000) == "₹25.0 K"


def test_calculate_emi():
    # 50 Lakhs at 8.5% for 20 years (240 months)
    emi = calculate_emi(5000000, 8.5, 240)
    # Standard formula value is ~43391.16
    assert round(emi, 2) == 43391.16

    # 10 Lakhs at 10% for 5 years (60 months)
    emi_car = calculate_emi(1000000, 10.0, 60)
    assert round(emi_car, 2) == 21247.04

    # Zero interest edge case
    assert calculate_emi(120000, 0.0, 12) == 10000.0


def test_loan_summary():
    summary = calculate_loan_summary(
        name="Test Loan",
        principal=1000000,
        annual_rate_pct=9.0,
        tenure_months=60,
        processing_fee_pct=1.0,
        documentation_charges=2000,
        gst_rate_pct=18.0
    )
    assert summary["principal"] == 1000000
    assert summary["processing_fee_base"] == 10000
    assert summary["documentation_charges"] == 2000
    assert summary["fee_gst"] == (12000 * 0.18)  # 2160
    assert summary["total_upfront_fees"] == 14160
    assert summary["net_disbursed"] == 1000000 - 14160
    # APR should be higher than nominal 9% due to upfront fees
    assert summary["effective_apr"] > 9.0


def test_amortization_schedule():
    df = generate_amortization_schedule(500000, 10.0, 12)
    assert len(df) == 12
    assert df.iloc[0]["Opening_Balance"] == 500000
    assert round(df.iloc[-1]["Closing_Balance"], 2) == 0.0
    assert round(df["Principal"].sum(), 2) == 500000.0

    annual = generate_annual_schedule(df)
    assert len(annual) == 1
    assert round(annual.iloc[0]["Principal_Paid"], 2) == 500000.0


def test_prepayment_simulation():
    # Prepaying extra ₹5,000/month should reduce tenure and save interest
    sim = simulate_prepayment(5000000, 8.5, 240, extra_monthly_payment=5000)
    assert sim["accelerated_tenure_months"] < 240
    assert sim["months_saved"] > 0
    assert sim["interest_saved"] > 500000


def test_affordability():
    afford = calculate_affordability(
        monthly_inhand_income=100000,
        existing_monthly_emis=10000,
        expected_rate_pct=8.5,
        desired_tenure_years=20,
        max_foir_pct=50.0
    )
    # 50% of 100k = 50k max total EMI. minus 10k existing = 40k available EMI.
    assert afford["max_allowable_total_emi"] == 50000
    assert afford["max_available_loan_emi"] == 40000
    assert afford["max_eligible_loan"] > 4000000
    assert afford["status"] == "Healthy / Ideal"


def test_presets_validity():
    for key, p in PRESETS.items():
        assert "loans" in p
        assert len(p["loans"]) >= 2
        for loan in p["loans"]:
            assert loan["principal"] > 0
            assert loan["annual_rate_pct"] > 0
            assert loan["tenure_months"] > 0


from utils.pdf_generator import generate_comparison_pdf
from utils.stress_tester import simulate_rate_hikes
from utils.tax_calculator import calculate_home_loan_tax_benefits


def test_stress_tester():
    stress = simulate_rate_hikes(5000000, 8.5, 240, [0.5, 1.0])
    assert len(stress["fixed_tenure_scenarios"]) == 2
    assert len(stress["fixed_emi_scenarios"]) == 2
    # +0.5% rate hike must increase monthly EMI
    assert stress["fixed_tenure_scenarios"][0]["emi_increase"] > 0
    # +0.5% rate hike must expand tenure if EMI is fixed
    assert stress["fixed_emi_scenarios"][0]["months_added"] > 0


def test_tax_calculator():
    tax_res = calculate_home_loan_tax_benefits(
        principal=5000000,
        annual_rate_pct=8.5,
        tenure_months=240,
        marginal_tax_slab_pct=30.0
    )
    assert tax_res["total_tax_saved"] > 0
    assert tax_res["effective_post_tax_rate"] < 8.5
    # First year interest deduction should not exceed ₹2,00,000 statutory cap
    assert tax_res["annual_tax_table"].iloc[0]["Sec_24b_Deduction"] <= 200000.0


def test_pdf_generation():
    s1 = calculate_loan_summary("Bank A", 5000000, 8.5, 240)
    s2 = calculate_loan_summary("Bank B", 5000000, 8.7, 240)
    pdf_bytes = generate_comparison_pdf([s1, s2], s1, s2)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")
