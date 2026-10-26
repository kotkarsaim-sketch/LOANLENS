"""
utils/tax_calculator.py - Indian Income Tax Shield Calculator (Section 24b & 80C)
Calculates annual tax savings and post-tax effective borrowing rates for Indian homeowners.
"""

from typing import Dict, Any, List
import pandas as pd
from utils.financial_engine import generate_amortization_schedule, generate_annual_schedule


def calculate_home_loan_tax_benefits(
    principal: float,
    annual_rate_pct: float,
    tenure_months: int,
    marginal_tax_slab_pct: float = 30.0,
    include_cess: bool = True
) -> Dict[str, Any]:
    """
    Computes tax savings under Section 24(b) (Interest cap: ₹2,00,000/yr)
    and Section 80C (Principal cap: ₹1,50,000/yr) under the Old Tax Regime.
    Tax bracket with 4% Health & Education Cess:
    - 30% slab -> 31.2% effective
    - 20% slab -> 20.8% effective
    - 10% slab -> 10.4% effective
    """
    effective_slab_rate = (marginal_tax_slab_pct * 1.04) / 100.0 if include_cess else (marginal_tax_slab_pct / 100.0)

    # Generate schedules
    monthly_df = generate_amortization_schedule(principal, annual_rate_pct, tenure_months)
    annual_df = generate_annual_schedule(monthly_df)

    if annual_df.empty:
        return {}

    tax_rows = []
    total_tax_saved = 0.0
    total_interest_paid = annual_df["Interest_Paid"].sum()

    for _, row in annual_df.iterrows():
        year = int(row["Year"])
        principal_paid = row["Principal_Paid"]
        interest_paid = row["Interest_Paid"]

        # Statutory Caps (Section 24b = ₹2L, Section 80C = ₹1.5L)
        deductible_interest = min(200000.0, interest_paid)
        deductible_principal = min(150000.0, principal_paid)

        tax_saved_interest = deductible_interest * effective_slab_rate
        tax_saved_principal = deductible_principal * effective_slab_rate
        year_total_tax_saved = tax_saved_interest + tax_saved_principal

        total_tax_saved += year_total_tax_saved

        tax_rows.append({
            "Year": year,
            "Principal_Repaid": principal_paid,
            "Interest_Paid": interest_paid,
            "Sec_24b_Deduction": deductible_interest,
            "Sec_80C_Deduction": deductible_principal,
            "Tax_Saved_Interest": tax_saved_interest,
            "Tax_Saved_Principal": tax_saved_principal,
            "Total_Tax_Saved": year_total_tax_saved,
            "Net_Effective_Outflow": (principal_paid + interest_paid) - year_total_tax_saved
        })

    tax_df = pd.DataFrame(tax_rows)

    # Post-tax effective interest calculation
    net_interest_after_tax = max(0.0, total_interest_paid - (tax_df["Tax_Saved_Interest"].sum()))
    tax_savings_ratio = (total_tax_saved / total_interest_paid * 100.0) if total_interest_paid > 0 else 0.0

    # Approximate post-tax effective interest rate
    effective_post_tax_rate = annual_rate_pct * (1.0 - (effective_slab_rate * min(1.0, 200000.0 / (principal * annual_rate_pct / 100.0)))) if principal > 0 else annual_rate_pct

    return {
        "annual_tax_table": tax_df,
        "total_tax_saved": total_tax_saved,
        "total_interest_tax_saved": tax_df["Tax_Saved_Interest"].sum(),
        "total_principal_tax_saved": tax_df["Tax_Saved_Principal"].sum(),
        "total_interest_paid": total_interest_paid,
        "net_interest_after_tax": net_interest_after_tax,
        "tax_savings_ratio": tax_savings_ratio,
        "effective_post_tax_rate": effective_post_tax_rate,
        "first_year_tax_saved": tax_df.iloc[0]["Total_Tax_Saved"] if not tax_df.empty else 0.0
    }
