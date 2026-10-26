"""
components/charts.py - Interactive Plotly charts for LoanLens
Theme: Light background with navy-blue (#0F2744 / #1E3A8A) accents and teal (#0D9488) highlights.
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.formatting import format_inr


def plot_cost_breakdown_donut(principal: float, total_interest: float, upfront_fees: float, loan_name: str = ""):
    """
    Donut chart breaking down Principal, Interest, and Upfront Fees.
    """
    labels = ["Principal Loan", "Total Interest", "Upfront Fees & GST"]
    values = [principal, total_interest, upfront_fees]
    colors = ["#1E3A8A", "#0D9488", "#F59E0B"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="percent",
                hoverinfo="label+value+percent",
                hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>"
            )
        ]
    )

    total_outflow = principal + total_interest + upfront_fees

    fig.update_layout(
        title=dict(
            text=f"Total Outflow Breakdown {f'({loan_name})' if loan_name else ''}",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        annotations=[
            dict(
                text=f"<span style='font-size:11px;color:#64748B;'>Total Outflow</span><br><b style='font-size:16px;color:#0F2744;'>{format_inr(total_outflow)}</b>",
                x=0.5, y=0.5,
                font_size=14,
                showarrow=False
            )
        ],
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=40, b=30),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_multi_loan_comparison(summaries: List[Dict[str, Any]]):
    """
    Stacked Bar Chart comparing Principal, Interest, and Fees across multiple loans.
    """
    names = [s["name"] for s in summaries]
    principals = [s["principal"] for s in summaries]
    interests = [s["total_interest"] for s in summaries]
    fees = [s["total_upfront_fees"] for s in summaries]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Principal",
        x=names,
        y=principals,
        marker_color="#1E3A8A",
        hovertemplate="<b>%{x}</b><br>Principal: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Total Interest",
        x=names,
        y=interests,
        marker_color="#0D9488",
        hovertemplate="<b>%{x}</b><br>Interest: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Upfront Fees & Taxes",
        x=names,
        y=fees,
        marker_color="#F59E0B",
        hovertemplate="<b>%{x}</b><br>Fees: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Total Borrowing Outflow Comparison (Stacked)",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="", tickfont=dict(color="#0F2744", size=12)),
        yaxis=dict(title="Total Outflow (₹)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_emi_comparison(summaries: List[Dict[str, Any]]):
    """
    Bar chart comparing monthly EMI across multiple offers.
    """
    names = [s["name"] for s in summaries]
    emis = [s["emi"] for s in summaries]

    # Find the min EMI to highlight with teal
    min_emi = min(emis)
    colors = ["#0D9488" if e == min_emi else "#1E3A8A" for e in emis]

    fig = go.Figure(
        data=[
            go.Bar(
                x=names,
                y=emis,
                marker=dict(color=colors, cornerradius=6),
                text=[format_inr(e) for e in emis],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Monthly EMI: ₹%{y:,.0f}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="Monthly EMI Commitment Comparison",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title=""),
        yaxis=dict(title="Monthly EMI (₹)", gridcolor="#E2E8F0"),
        margin=dict(l=20, r=20, t=45, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_amortization_balance_trajectory(amort_df: pd.DataFrame, loan_name: str = ""):
    """
    Line chart showing loan principal balance trajectory over tenure.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=amort_df["Month"],
        y=amort_df["Closing_Balance"],
        mode="lines",
        name="Outstanding Balance",
        line=dict(color="#0F2744", width=3),
        fill="tozeroy",
        fillcolor="rgba(15, 39, 68, 0.05)",
        hovertemplate="Month %{x}<br>Outstanding Balance: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=amort_df["Month"],
        y=amort_df["Cumulative_Interest"],
        mode="lines",
        name="Cumulative Interest Paid",
        line=dict(color="#0D9488", width=2.5, dash="dash"),
        hovertemplate="Month %{x}<br>Total Interest Paid: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"Amortization Trajectory {f'({loan_name})' if loan_name else ''}",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="Loan Month", gridcolor="#E2E8F0"),
        yaxis=dict(title="Rupees (₹)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_annual_principal_vs_interest(annual_df: pd.DataFrame):
    """
    Stacked bar chart of Annual Principal vs Annual Interest Paid.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Principal Repaid",
        x=annual_df["Year"],
        y=annual_df["Principal_Paid"],
        marker_color="#1E3A8A",
        hovertemplate="Year %{x}<br>Principal Paid: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Interest Paid",
        x=annual_df["Year"],
        y=annual_df["Interest_Paid"],
        marker_color="#0D9488",
        hovertemplate="Year %{x}<br>Interest Paid: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Annual Repayment Composition (Principal vs Interest)",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="Year", tickmode="linear", dtick=1),
        yaxis=dict(title="Amount Paid (₹)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_prepayment_comparison(original_df: pd.DataFrame, accelerated_df: pd.DataFrame):
    """
    Compare standard amortization balance curve vs accelerated prepayment payoff curve.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=original_df["Month"],
        y=original_df["Closing_Balance"],
        mode="lines",
        name="Standard Payoff Schedule",
        line=dict(color="#64748B", width=2, dash="dash"),
        hovertemplate="Month %{x}<br>Standard Balance: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=accelerated_df["Month"],
        y=accelerated_df["Closing_Balance"],
        mode="lines",
        name="Accelerated Prepayment Schedule",
        line=dict(color="#0D9488", width=3),
        fill="tonexty",
        fillcolor="rgba(13, 148, 136, 0.1)",
        hovertemplate="Month %{x}<br>Accelerated Balance: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="Payoff Acceleration Timeline (Time & Debt Reduction)",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="Tenure in Months", gridcolor="#E2E8F0"),
        yaxis=dict(title="Outstanding Loan Balance (₹)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_rate_vs_apr(summaries: List[Dict[str, Any]]):
    """
    Bar chart showing Nominal Interest Rate vs True Effective APR.
    """
    names = [s["name"] for s in summaries]
    nominal_rates = [s["annual_rate_pct"] for s in summaries]
    aprs = [s["effective_apr"] for s in summaries]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Advertised Nominal Rate",
        x=names,
        y=nominal_rates,
        marker_color="#1E3A8A",
        text=[f"{r:.2f}%" for r in nominal_rates],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Nominal: %{y:.2f}%<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="True Effective APR (inc. Fees)",
        x=names,
        y=aprs,
        marker_color="#0D9488",
        text=[f"{a:.2f}%" for a in aprs],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Effective APR: %{y:.2f}%<extra></extra>"
    ))

    fig.update_layout(
        barmode="group",
        title=dict(
            text="Transparency Check: Advertised Rate vs Real Effective APR",
            font=dict(size=15, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title=""),
        yaxis=dict(title="Annual Rate (%)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=50, b=20),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_rate_hike_sensitivity(stress_results: Dict[str, Any]):
    """
    Plot rate hike impact on EMI (Fixed Tenure) and Tenure Extension (Fixed EMI).
    """
    fixed_tenure = stress_results["fixed_tenure_scenarios"]
    rate_labels = [f"+{s['rate_delta']:.2f}%\n({s['new_rate_pct']:.2f}%)" for s in fixed_tenure]
    emi_increases = [s["emi_increase"] for s in fixed_tenure]

    fig = go.Figure(
        data=[
            go.Bar(
                x=rate_labels,
                y=emi_increases,
                marker=dict(color="#EF4444", cornerradius=6),
                text=[f"+₹{val:,.0f}" for val in emi_increases],
                textposition="outside",
                hovertemplate="Rate Hike %{x}<br>Monthly EMI Increase: +₹%{y:,.0f}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="Monthly EMI Shock under RBI Rate Hikes (Fixed Tenure)",
            font=dict(size=14, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="Repo Rate Hike (New Nominal Rate)"),
        yaxis=dict(title="Additional Monthly EMI (₹)", gridcolor="#E2E8F0"),
        margin=dict(l=20, r=20, t=45, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_tax_shield_breakdown(tax_df: pd.DataFrame):
    """
    Plot annual tax savings under Sec 24(b) (Interest) and Sec 80C (Principal).
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Sec 24(b) Interest Tax Shield (Cap ₹2L)",
        x=tax_df["Year"],
        y=tax_df["Tax_Saved_Interest"],
        marker_color="#0D9488",
        hovertemplate="Year %{x}<br>Interest Tax Saved: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Sec 80C Principal Tax Shield (Cap ₹1.5L)",
        x=tax_df["Year"],
        y=tax_df["Tax_Saved_Principal"],
        marker_color="#1E3A8A",
        hovertemplate="Year %{x}<br>Principal Tax Saved: ₹%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Annual Tax Rebate Shield (Old Tax Regime @ 30% Slab)",
            font=dict(size=14, color="#0F2744", family="Plus Jakarta Sans"),
            x=0.0
        ),
        xaxis=dict(title="Loan Year", tickmode="linear", dtick=1),
        yaxis=dict(title="Annual Tax Saved (₹)", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        margin=dict(l=20, r=20, t=45, b=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig
