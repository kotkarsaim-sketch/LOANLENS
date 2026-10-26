"""
components/ui_components.py - Reusable UI widgets and presentation cards for LoanLens
Follows navy-blue (#0F2744) accents with subtle teal (#0D9488) highlights and light card backgrounds.
"""

import streamlit as st
from utils.formatting import format_inr, format_inr_compact, format_percent, format_tenure_display
from typing import Dict, Any, List


def render_header():
    """Render top application banner"""
    st.markdown(
        """
        <div class="app-header">
            <div>
                <h1>LoanLens</h1>
                <p>Intelligent Loan Comparison, Cost-of-Credit Modeling & Amortization Intelligence</p>
            </div>
            <div style="text-align: right;">
                <span class="app-badge">Fintech Academic Edition</span>
                <p style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.35rem;">Live Mathematical Modeling</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str, subtext: str = "", delta_type: str = "neutral"):
    """
    Render a styled card with KPI metric.
    delta_type: 'positive' (teal/green), 'negative' (red), 'neutral' (navy/slate)
    """
    sub_color = "#0D9488" if delta_type == "positive" else ("#EF4444" if delta_type == "negative" else "#64748B")
    card_html = f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        {f'<div class="subtext" style="color: {sub_color};">{subtext}</div>' if subtext else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_winner_banner(winner_summary: Dict[str, Any], runner_up_summary: Dict[str, Any] = None):
    """
    Renders an eye-catching recommendation banner for the lowest total cost loan.
    """
    name = winner_summary["name"]
    total_cost = winner_summary["total_cost_of_credit"]
    emi = winner_summary["emi"]
    apr = winner_summary["effective_apr"]

    savings_html = ""
    if runner_up_summary and runner_up_summary["total_cost_of_credit"] > total_cost:
        delta = runner_up_summary["total_cost_of_credit"] - total_cost
        savings_html = f"""
        <div style="background: rgba(16, 185, 129, 0.15); padding: 0.5rem 1rem; border-radius: 8px; display: inline-block; margin-top: 0.5rem;">
            <strong style="color: #065F46;">Estimated Savings:</strong> 
            <span style="font-weight: 800; color: #047857; font-size: 1.1rem;">{format_inr(delta)}</span> 
            <span style="font-size: 0.85rem; color: #065F46;">over {runner_up_summary['name']}</span>
        </div>
        """

    st.markdown(
        f"""
        <div class="winner-card">
            <span class="winner-tag">🏆 Best Overall Financial Value</span>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h3 style="margin: 0; font-size: 1.45rem; color: #064E3B; font-weight: 800;">{name}</h3>
                    <p style="margin: 0.25rem 0 0 0; color: #047857; font-size: 0.9rem;">
                        Lowest Total Cost of Borrowing with competitive APR & transparent fee structure.
                    </p>
                    {savings_html}
                </div>
                <div style="display: flex; gap: 1.5rem; text-align: right;">
                    <div>
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: #065F46; font-weight: 700;">Monthly EMI</div>
                        <div style="font-size: 1.35rem; font-weight: 800; color: #064E3B;">{format_inr(emi)}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: #065F46; font-weight: 700;">Total Cost of Credit</div>
                        <div style="font-size: 1.35rem; font-weight: 800; color: #047857;">{format_inr(total_cost)}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: #065F46; font-weight: 700;">Effective APR</div>
                        <div style="font-size: 1.35rem; font-weight: 800; color: #0D9488;">{format_percent(apr)}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_loan_card(summary: Dict[str, Any], is_winner: bool = False):
    """
    Render a clean white card presenting single loan offer breakdown
    """
    border_style = "2px solid #10B981" if is_winner else "1px solid #E2E8F0"
    badge_html = '<span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; margin-left: 8px;">TOP PICK</span>' if is_winner else ''

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: {border_style}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #0F2744; font-size: 1.15rem; font-weight: 700;">{summary['name']}{badge_html}</h4>
                <span style="font-size: 0.85rem; font-weight: 700; color: #0D9488; background: #F0FDFA; padding: 3px 10px; border-radius: 6px;">
                    {format_percent(summary['annual_rate_pct'])} p.a.
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; font-size: 0.85rem; border-top: 1px solid #F1F5F9; padding-top: 0.75rem;">
                <div>
                    <span style="color: #64748B;">Monthly EMI:</span><br>
                    <strong style="color: #0F2744; font-size: 1.05rem;">{format_inr(summary['emi'])}</strong>
                </div>
                <div>
                    <span style="color: #64748B;">Effective APR:</span><br>
                    <strong style="color: #0F2744; font-size: 1.05rem;">{format_percent(summary['effective_apr'])}</strong>
                </div>
                <div>
                    <span style="color: #64748B;">Total Interest:</span><br>
                    <strong style="color: #475569;">{format_inr(summary['total_interest'])}</strong>
                </div>
                <div>
                    <span style="color: #64748B;">Upfront Fees (inc. GST):</span><br>
                    <strong style="color: #475569;">{format_inr(summary['total_upfront_fees'])}</strong>
                </div>
                <div style="grid-column: span 2; background: #F8FAFC; padding: 0.6rem 0.75rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #0F2744;">Total Cost of Borrowing:</span>
                    <span style="font-weight: 800; color: #0F2744; font-size: 1rem;">{format_inr(summary['total_cost_of_credit'])}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
