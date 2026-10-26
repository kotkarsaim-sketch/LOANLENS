"""
utils/financial_engine.py - Core Financial Mathematics Engine for LoanLens
Includes accurate reducing balance EMI, complete amortization schedules,
APR (Annual Percentage Rate) solver, prepayment simulations, and affordability analysis.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


def calculate_emi(principal: float, annual_rate_pct: float, tenure_months: int) -> float:
    """
    Calculate Monthly Reducing Balance Equated Monthly Installment (EMI).
    Formula: EMI = [P x r x (1+r)^n] / [(1+r)^n - 1]
    where:
      P = Principal loan amount
      r = Monthly interest rate (annual rate / 12 / 100)
      n = Tenure in months
    """
    if tenure_months <= 0 or principal <= 0:
        return 0.0

    monthly_rate = (annual_rate_pct / 100.0) / 12.0

    if monthly_rate == 0:
        return principal / tenure_months

    compounded = (1.0 + monthly_rate) ** tenure_months
    emi = principal * monthly_rate * compounded / (compounded - 1.0)
    return emi


def solve_apr(principal: float, emi: float, tenure_months: int, upfront_fees: float) -> float:
    """
    Calculate the True Annual Percentage Rate (APR) / Internal Rate of Return (IRR).
    Accounts for net disbursed amount = (Principal - Upfront Fees)
    Equation solved: Net_Disbursed = sum_{t=1}^n [ EMI / (1 + r)^t ]
    Returns annualized rate in percent.
    """
    if principal <= 0 or emi <= 0 or tenure_months <= 0:
        return 0.0

    net_disbursed = principal - upfront_fees
    if net_disbursed <= 0:
        return 0.0

    # If no upfront fees, APR matches nominal rate approximately
    # Binary search for monthly rate r
    low = 0.000001
    high = 1.0  # up to 100% per month

    def npv(r: float) -> float:
        # Sum of discounted cashflows
        # using closed form sum of geometric series:
        # EMI * [1 - (1+r)^-n] / r
        if r == 0:
            return emi * tenure_months
        return (emi / r) * (1.0 - (1.0 + r) ** (-tenure_months))

    for _ in range(60):
        mid = (low + high) / 2.0
        val = npv(mid)
        if abs(val - net_disbursed) < 1e-4:
            break
        if val > net_disbursed:
            low = mid
        else:
            high = mid

    monthly_r = (low + high) / 2.0
    nominal_annual_apr = monthly_r * 12.0 * 100.0
    return nominal_annual_apr


def calculate_loan_summary(
    name: str,
    principal: float,
    annual_rate_pct: float,
    tenure_months: int,
    processing_fee_pct: float = 0.0,
    processing_fee_flat: float = 0.0,
    documentation_charges: float = 0.0,
    insurance_charges: float = 0.0,
    gst_rate_pct: float = 18.0
) -> Dict[str, Any]:
    """
    Generate comprehensive loan cost summary including all upfront fees, GST,
    total interest, APR, and metrics.
    """
    emi = calculate_emi(principal, annual_rate_pct, tenure_months)
    total_repayment = emi * tenure_months
    total_interest = max(0.0, total_repayment - principal)

    # Calculate processing fee
    fee_from_pct = (principal * processing_fee_pct) / 100.0
    processing_fee_base = fee_from_pct + processing_fee_flat

    # GST on processing and documentation fees (standard 18% in India)
    taxable_fees = processing_fee_base + documentation_charges
    fee_gst = (taxable_fees * gst_rate_pct) / 100.0

    total_upfront_fees = taxable_fees + fee_gst + insurance_charges
    net_disbursed = principal - total_upfront_fees
    total_cost_of_credit = total_interest + total_upfront_fees
    total_outflow = principal + total_cost_of_credit

    apr = solve_apr(principal, emi, tenure_months, total_upfront_fees)

    interest_ratio = (total_interest / principal * 100.0) if principal > 0 else 0.0
    fee_ratio = (total_upfront_fees / principal * 100.0) if principal > 0 else 0.0

    return {
        "name": name,
        "principal": principal,
        "annual_rate_pct": annual_rate_pct,
        "tenure_months": tenure_months,
        "tenure_years": tenure_months / 12.0,
        "emi": emi,
        "total_repayment": total_repayment,
        "total_interest": total_interest,
        "processing_fee_base": processing_fee_base,
        "documentation_charges": documentation_charges,
        "insurance_charges": insurance_charges,
        "fee_gst": fee_gst,
        "total_upfront_fees": total_upfront_fees,
        "net_disbursed": net_disbursed,
        "total_cost_of_credit": total_cost_of_credit,
        "total_outflow": total_outflow,
        "interest_ratio": interest_ratio,
        "fee_ratio": fee_ratio,
        "effective_apr": apr,
        "apr_difference": apr - annual_rate_pct
    }


def generate_amortization_schedule(
    principal: float,
    annual_rate_pct: float,
    tenure_months: int
) -> pd.DataFrame:
    """
    Generate month-by-month reducing balance amortization schedule.
    """
    if principal <= 0 or tenure_months <= 0:
        return pd.DataFrame()

    emi = calculate_emi(principal, annual_rate_pct, tenure_months)
    monthly_rate = (annual_rate_pct / 100.0) / 12.0

    rows = []
    balance = principal
    cumulative_interest = 0.0
    cumulative_principal = 0.0

    for m in range(1, tenure_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = emi - interest_payment

        # Handle last month rounding
        if m == tenure_months or principal_payment > balance:
            principal_payment = balance
            emi_actual = principal_payment + interest_payment
            closing_balance = 0.0
        else:
            emi_actual = emi
            closing_balance = max(0.0, balance - principal_payment)

        cumulative_interest += interest_payment
        cumulative_principal += principal_payment

        year_num = (m - 1) // 12 + 1
        month_in_year = (m - 1) % 12 + 1

        rows.append({
            "Month": m,
            "Year": year_num,
            "Month_in_Year": month_in_year,
            "Opening_Balance": balance,
            "EMI": emi_actual,
            "Principal": principal_payment,
            "Interest": interest_payment,
            "Closing_Balance": closing_balance,
            "Cumulative_Principal": cumulative_principal,
            "Cumulative_Interest": cumulative_interest,
            "Principal_Pct": (principal_payment / emi_actual * 100.0) if emi_actual > 0 else 0,
            "Interest_Pct": (interest_payment / emi_actual * 100.0) if emi_actual > 0 else 0,
        })

        balance = closing_balance
        if balance <= 0:
            break

    df = pd.DataFrame(rows)
    return df


def generate_annual_schedule(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate monthly amortization table into annual summary.
    """
    if monthly_df.empty:
        return pd.DataFrame()

    grouped = monthly_df.groupby("Year")
    annual_data = []

    for year, group in grouped:
        opening_bal = group.iloc[0]["Opening_Balance"]
        closing_bal = group.iloc[-1]["Closing_Balance"]
        total_emi = group["EMI"].sum()
        total_principal = group["Principal"].sum()
        total_interest = group["Interest"].sum()
        cum_interest = group.iloc[-1]["Cumulative_Interest"]
        cum_principal = group.iloc[-1]["Cumulative_Principal"]

        annual_data.append({
            "Year": int(year),
            "Opening_Balance": opening_bal,
            "Total_EMI": total_emi,
            "Principal_Paid": total_principal,
            "Interest_Paid": total_interest,
            "Closing_Balance": closing_bal,
            "Cumulative_Principal": cum_principal,
            "Cumulative_Interest": cum_interest,
        })

    return pd.DataFrame(annual_data)


def simulate_prepayment(
    principal: float,
    annual_rate_pct: float,
    tenure_months: int,
    extra_monthly_payment: float = 0.0,
    lump_sum_amount: float = 0.0,
    lump_sum_month: int = 12
) -> Dict[str, Any]:
    """
    Simulate impact of extra monthly prepayment and/or one-time lump-sum prepayment.
    Calculates months saved, interest saved, and comparative schedules.
    """
    standard_emi = calculate_emi(principal, annual_rate_pct, tenure_months)
    monthly_rate = (annual_rate_pct / 100.0) / 12.0

    # Baseline standard schedule
    std_df = generate_amortization_schedule(principal, annual_rate_pct, tenure_months)
    baseline_interest = std_df["Interest"].sum() if not std_df.empty else 0.0

    # Accelerated schedule
    balance = principal
    acc_rows = []
    month = 0
    cum_interest = 0.0
    cum_principal = 0.0

    max_safety_months = tenure_months + 120  # Safeguard

    while balance > 0.01 and month < max_safety_months:
        month += 1
        interest_payment = balance * monthly_rate

        # Regular EMI + extra monthly
        target_payment = standard_emi + extra_monthly_payment

        # Add lump sum if this is the target month
        lump_this_month = 0.0
        if month == lump_sum_month and lump_sum_amount > 0:
            lump_this_month = lump_sum_amount
            target_payment += lump_this_month

        available_for_principal = target_payment - interest_payment

        if available_for_principal >= balance:
            # Final payoff
            principal_paid = balance
            actual_emi = principal_paid + interest_payment
            closing_balance = 0.0
        else:
            principal_paid = available_for_principal
            actual_emi = target_payment
            closing_balance = balance - principal_paid

        cum_interest += interest_payment
        cum_principal += principal_paid

        acc_rows.append({
            "Month": month,
            "Opening_Balance": balance,
            "Regular_EMI": standard_emi,
            "Extra_Payment": extra_monthly_payment + lump_this_month,
            "Total_Paid": actual_emi,
            "Principal_Paid": principal_paid,
            "Interest_Paid": interest_payment,
            "Closing_Balance": closing_balance,
            "Cumulative_Interest": cum_interest
        })

        balance = closing_balance

    acc_df = pd.DataFrame(acc_rows)
    accelerated_tenure_months = len(acc_rows)
    accelerated_interest = cum_interest

    months_saved = max(0, tenure_months - accelerated_tenure_months)
    interest_saved = max(0.0, baseline_interest - accelerated_interest)
    pct_interest_saved = (interest_saved / baseline_interest * 100.0) if baseline_interest > 0 else 0.0

    return {
        "original_tenure_months": tenure_months,
        "accelerated_tenure_months": accelerated_tenure_months,
        "months_saved": months_saved,
        "years_saved": months_saved / 12.0,
        "original_interest": baseline_interest,
        "accelerated_interest": accelerated_interest,
        "interest_saved": interest_saved,
        "pct_interest_saved": pct_interest_saved,
        "original_schedule": std_df,
        "accelerated_schedule": acc_df,
        "total_extra_contributed": (extra_monthly_payment * accelerated_tenure_months) + (lump_sum_amount if accelerated_tenure_months >= lump_sum_month else 0.0)
    }


def calculate_affordability(
    monthly_inhand_income: float,
    existing_monthly_emis: float,
    expected_rate_pct: float,
    desired_tenure_years: int,
    max_foir_pct: float = 50.0
) -> Dict[str, Any]:
    """
    Calculate maximum loan borrowing capacity based on FOIR (Fixed Obligation to Income Ratio).
    FOIR standard across Indian banks is 40% - 50%.
    """
    tenure_months = int(desired_tenure_years * 12)
    max_allowable_total_emi = monthly_inhand_income * (max_foir_pct / 100.0)
    max_available_loan_emi = max(0.0, max_allowable_total_emi - existing_monthly_emis)

    # Derive principal capacity from EMI
    # P = EMI * [(1+r)^n - 1] / [r * (1+r)^n]
    monthly_rate = (expected_rate_pct / 100.0) / 12.0

    if monthly_rate == 0:
        max_eligible_loan = max_available_loan_emi * tenure_months
    else:
        factor = (1.0 + monthly_rate) ** tenure_months
        max_eligible_loan = max_available_loan_emi * (factor - 1.0) / (monthly_rate * factor)

    current_foir = (existing_monthly_emis / monthly_inhand_income * 100.0) if monthly_inhand_income > 0 else 0.0

    # Risk level categorization
    if current_foir > 50.0:
        status = "High Risk"
        status_color = "#EF4444"
        advice = "Your existing debt obligations exceed 50% of your income. Lenders may reject new applications or charge risk premiums."
    elif current_foir > 35.0:
        status = "Moderate / Stretched"
        status_color = "#F59E0B"
        advice = "Your existing debt is moderate. You have modest additional borrowing capacity."
    else:
        status = "Healthy / Ideal"
        status_color = "#10B981"
        advice = "Your debt-to-income profile is comfortable. You have strong eligibility for competitive prime lending rates."

    return {
        "monthly_income": monthly_inhand_income,
        "existing_emis": existing_monthly_emis,
        "max_foir_pct": max_foir_pct,
        "max_allowable_total_emi": max_allowable_total_emi,
        "max_available_loan_emi": max_available_loan_emi,
        "max_eligible_loan": max_eligible_loan,
        "current_foir": current_foir,
        "status": status,
        "status_color": status_color,
        "advice": advice
    }


def find_loan_winner(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze multiple loan summaries and determine optimal recommendations.
    Identifies lowest total cost, lowest EMI, lowest APR, and calculates savings deltas.
    """
    if not summaries:
        return {}

    lowest_cost = min(summaries, key=lambda s: s["total_cost_of_credit"])
    highest_cost = max(summaries, key=lambda s: s["total_cost_of_credit"])
    lowest_emi = min(summaries, key=lambda s: s["emi"])
    lowest_apr = min(summaries, key=lambda s: s["effective_apr"])

    cost_savings = highest_cost["total_cost_of_credit"] - lowest_cost["total_cost_of_credit"]

    return {
        "winner_by_total_cost": lowest_cost,
        "winner_by_emi": lowest_emi,
        "winner_by_apr": lowest_apr,
        "cost_savings_vs_worst": cost_savings,
        "most_expensive": highest_cost,
    }
