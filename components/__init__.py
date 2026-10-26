"""
Components package for LoanLens
"""
from components.ui_components import render_header, render_metric_card, render_winner_banner, render_loan_card
from components.charts import (
    plot_cost_breakdown_donut,
    plot_multi_loan_comparison,
    plot_emi_comparison,
    plot_amortization_balance_trajectory,
    plot_annual_principal_vs_interest,
    plot_prepayment_comparison,
    plot_rate_vs_apr,
    plot_rate_hike_sensitivity,
    plot_tax_shield_breakdown
)
