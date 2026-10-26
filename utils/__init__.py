"""
Utils package for LoanLens
"""
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
from utils.pdf_generator import generate_comparison_pdf
from utils.stress_tester import simulate_rate_hikes
from utils.tax_calculator import calculate_home_loan_tax_benefits
