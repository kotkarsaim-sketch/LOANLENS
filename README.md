# ⚖️ LoanLens — Smart Loan Comparison & Financial Intelligence Platform

> **Academic Project Prototype — Fintech & Financial Engineering Edition**  
> Built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. Zero external database or paid API dependencies.

---

## 🌟 Executive Summary

Retail borrowers frequently struggle to identify the most cost-effective loan offer. Lenders advertise attractive headline interest rates while embedding hidden costs such as processing fees, administrative charges, document costs, and mandatory **18% Goods & Services Tax (GST)**. 

**LoanLens** is a modern, transparent fintech web application designed to solve this problem. It equips consumers, students, and financial analysts with institutional-grade computational tools to:
1. **Compare multiple loan offers side-by-side** and automatically identify the **lowest total borrowing cost** and savings deltas.
2. **Expose hidden fees** by calculating the true **Effective Annual Percentage Rate (APR)** using discounted cash flow root-solving.
3. **Explore full month-by-month and annual amortization schedules** with interactive visualization of reducing-balance decay.
4. **Model debt acceleration strategies** (extra monthly EMIs or lump-sum prepayments) to quantify exact months and lakhs of rupees saved.
5. **Stress-test floating-rate loans against RBI repo rate hikes** under both Fixed Tenure and Fixed EMI banking policies.
6. **Model government tax deductions** under Indian Income Tax Act (Section 24b up to ₹2L & Section 80C up to ₹1.5L) to compute net post-tax borrowing costs.
7. **Assess borrowing affordability** using the Indian banking industry standard **FOIR (Fixed Obligation to Income Ratio)** rule.
8. **Export executive evaluation reports** to both CSV and publication-ready **PDF**.

---

## 🚀 Quickstart: Run in 1 Command

Ensure Python 3.10+ is installed. Then launch directly from the project directory:

```bash
streamlit run app.py
```

*Alternative Windows launchers:*
```powershell
# Using Python module runner:
python -m streamlit run app.py

# Or double-click the included batch launcher:
.\run.bat
```

Open your browser at `http://localhost:8501`.

---

## 📐 Financial Engineering & Mathematical Engine

### 1. Reducing Balance Equated Monthly Installment (EMI)
Calculates monthly debt service where interest is calculated only on the remaining balance:
$$\text{EMI} = P \times r \times \frac{(1+r)^n}{(1+r)^n - 1}$$
* $P$ = Principal loan amount
* $r = \frac{\text{Annual Nominal Rate}}{12 \times 100}$ (Monthly periodic interest rate)
* $n = \text{Tenure in months}$

### 2. True Effective APR (Annual Percentage Rate) Solver
Standard advertised rates conceal upfront cash deductions. LoanLens computes the true IRR $r_{\text{eff}}$ by equating the **net cash disbursed** on Day 0 with discounted future EMI payments:
$$\text{Principal} - \text{Total Upfront Fees \& GST} = \sum_{t=1}^n \frac{\text{EMI}}{(1 + r_{\text{eff}})^t}$$
The annualized APR is:
$$\text{APR} = r_{\text{eff}} \times 12 \times 100$$

### 3. Prepayment Debt Acceleration Simulation
Simulates continuous monthly balance recalculation:
$$\text{Principal Repayment}_m = \text{Regular EMI} + \text{Extra Payment}_m - (\text{Balance}_{m-1} \times r)$$
Quantifies the exact reduction in borrowing tenure and interest saved.

### 4. Floating Rate Stress Testing Formulations
Under Policy 1 (Fixed Tenure), the adjusted EMI is calculated using $r_{\text{new}} = r_{\text{current}} + \Delta r$.  
Under Policy 2 (Fixed EMI), the expanded tenure $n_{\text{new}}$ is derived analytically:
$$n_{\text{new}} = -\frac{\ln\left(1 - \frac{P \cdot r_{\text{new}}}{\text{EMI}_{\text{base}}}\right)}{\ln(1 + r_{\text{new}})}$$
If $P \cdot r_{\text{new}} \ge \text{EMI}_{\text{base}}$, the loan enters a **negative amortization trap**, where interest accrues faster than repayment!

### 5. Indian Home Loan Tax Shield (Section 24b & 80C)
Computes statutory tax shields under the Old Tax Regime:
$$\text{Tax Deduction}_{\text{annual}} = \min(₹2,00,000, \text{Interest Paid}) + \min(₹1,50,000, \text{Principal Repaid})$$
$$\text{Tax Refund} = \text{Tax Deduction} \times \text{Marginal Tax Bracket (inc. 4\% cess)}$$

### 6. FOIR (Fixed Obligation to Income Ratio) Affordability
Indian retail banks enforce an upper debt ceiling (typically 40% to 50% of net monthly income):
$$\text{Max Allowable EMI} = (\text{Net Monthly Salary} \times \text{FOIR \%}) - \text{Existing Debt Obligations}$$
$$\text{Max Borrowing Capacity} = \text{Max Allowable EMI} \times \frac{(1+r)^n - 1}{r(1+r)^n}$$

---

## 🗂️ Application Architecture

```
FLB/
├── app.py                     # Main Streamlit web application & router
├── config.py                  # Typography, custom CSS, fintech color palette
├── run.bat                    # 1-click Windows launcher
├── run.ps1                    # 1-click PowerShell launcher
├── requirements.txt           # Project dependencies
├── utils/
│   ├── __init__.py
│   ├── financial_engine.py    # Core math: EMI, APR solver, schedules, prepayments
│   ├── formatting.py          # Indian Rupee (₹, Lakhs, Crores, commas) formatter
│   ├── pdf_generator.py       # Professional PDF executive report generator (fpdf2)
│   ├── stress_tester.py       # Floating rate sensitivity & RBI hike simulator
│   ├── tax_calculator.py      # Indian Income Tax deductions (Sec 24b & 80C)
│   └── presets.py             # Curated real-world bank presets (SBI, HDFC, ICICI, etc.)
├── components/
│   ├── __init__.py
│   ├── ui_components.py       # Reusable KPI cards, winner banners, custom containers
│   └── charts.py              # Interactive Plotly visual charts
└── tests/
    └── test_loanlens.py       # Pytest unit & regression test suite (11/11 passing, 0 warnings)
```

---

## 🎨 UI/UX & Design Philosophy

* **Fintech Palette:** Crisp light background (`#F8FAFC`) with deep navy accents (`#0F2744`) and subtle teal highlights (`#0D9488`).
* **Indian Rupee Standard:** Strict adherence to Indian numbering conventions (e.g., `₹50,00,000` / `₹50.00 L` instead of western million groupings).
* **Live Dynamic Recalculation:** Instant state updates on slider/input changes without manual page refreshes.
* **Winner Identification:** Clear visual winner badge displaying total cost differences and rupee savings vs competitor offers.

---

## 🧪 Verification & Automated Testing

A dedicated test suite is provided in `tests/test_loanlens.py`. Run tests using:

```bash
python -m pytest tests/test_loanlens.py -v
```

**Test Coverage (11/11 Passing):**
- ✅ Indian Rupee comma grouping and compact notation (Thousand, Lakh, Crore, Negative values)
- ✅ Reducing balance EMI numerical accuracy against institutional benchmarks
- ✅ APR root-finding bisection convergence under varied upfront fee percentages
- ✅ Full 240-month and 60-month amortization schedule balance convergence to ₹0.00
- ✅ Prepayment acceleration savings calculation
- ✅ FOIR debt affordability risk categorization
- ✅ Bank preset integrity and parameter bounds
- ✅ Floating-rate stress tester (Fixed Tenure & Fixed EMI)
- ✅ Section 24(b) & 80C statutory deduction caps
- ✅ Formal PDF report generation binary integrity
