"""
utils/stress_tester.py - Floating Rate Stress Testing & RBI Rate Hike Simulator
Analyzes interest rate sensitivity across both fixed-tenure and fixed-EMI banking practices.
"""

from typing import Dict, Any, List
import math
from utils.financial_engine import calculate_emi


def simulate_rate_hikes(
    principal: float,
    current_rate_pct: float,
    tenure_months: int,
    rate_hike_deltas: List[float] = [0.25, 0.50, 1.00, 1.50, 2.00]
) -> Dict[str, Any]:
    """
    Simulate impact of rate hikes under two realistic banking policies:
    1. Fixed Tenure Policy: EMI increases to keep tenure constant.
    2. Fixed EMI Policy: EMI stays constant while tenure expands.
    """
    base_emi = calculate_emi(principal, current_rate_pct, tenure_months)
    base_total_interest = (base_emi * tenure_months) - principal

    fixed_tenure_scenarios = []
    fixed_emi_scenarios = []

    for delta in rate_hike_deltas:
        new_rate = current_rate_pct + delta
        new_monthly_r = (new_rate / 100.0) / 12.0

        # Scenario 1: Fixed Tenure (EMI Rises)
        new_emi = calculate_emi(principal, new_rate, tenure_months)
        new_total_interest = (new_emi * tenure_months) - principal
        emi_increase = new_emi - base_emi
        extra_interest = new_total_interest - base_total_interest

        fixed_tenure_scenarios.append({
            "rate_delta": delta,
            "new_rate_pct": new_rate,
            "new_emi": new_emi,
            "emi_increase": emi_increase,
            "new_total_interest": new_total_interest,
            "extra_interest": extra_interest,
            "pct_emi_increase": (emi_increase / base_emi * 100.0) if base_emi > 0 else 0
        })

        # Scenario 2: Fixed EMI (Tenure Expands)
        # Solve for n where EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        # 1 - (P * r / EMI) = (1+r)^-n
        # -n = ln(1 - P * r / EMI) / ln(1+r)
        # If P * r >= EMI, loan never amortizes (negative amortization trap!)
        if principal * new_monthly_r >= base_emi:
            expanded_months = math.inf
            months_added = math.inf
            extended_interest = math.inf
            is_trap = True
        else:
            ratio = 1.0 - (principal * new_monthly_r / base_emi)
            if ratio > 0:
                n_float = -math.log(ratio) / math.log(1.0 + new_monthly_r)
                expanded_months = int(math.ceil(n_float))
                months_added = max(0, expanded_months - tenure_months)
                extended_interest = (base_emi * expanded_months) - principal
                is_trap = False
            else:
                expanded_months = math.inf
                months_added = math.inf
                extended_interest = math.inf
                is_trap = True

        fixed_emi_scenarios.append({
            "rate_delta": delta,
            "new_rate_pct": new_rate,
            "fixed_emi": base_emi,
            "expanded_tenure_months": expanded_months,
            "months_added": months_added,
            "years_added": (months_added / 12.0) if not is_trap else None,
            "extended_total_interest": extended_interest,
            "extra_interest": (extended_interest - base_total_interest) if not is_trap else None,
            "is_negative_amortization_trap": is_trap
        })

    return {
        "base_rate": current_rate_pct,
        "base_emi": base_emi,
        "base_tenure_months": tenure_months,
        "base_total_interest": base_total_interest,
        "fixed_tenure_scenarios": fixed_tenure_scenarios,
        "fixed_emi_scenarios": fixed_emi_scenarios
    }
