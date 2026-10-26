"""
utils/formatting.py - Indian Rupee (INR) formatting utilities
Supports standard Indian comma system (2, 2, 3 grouping) and compact Lakh/Crore notation.
"""

def format_inr(amount: float, include_symbol: bool = True, decimals: int = 0) -> str:
    """
    Format a number using the Indian numbering grouping system:
    e.g., 1000000 -> ₹10,00,000
    e.g., 12345678.5 -> ₹1,23,45,678.50
    """
    if amount is None:
        return "₹0" if include_symbol else "0"
    
    try:
        val = float(amount)
    except (ValueError, TypeError):
        return str(amount)

    is_negative = val < 0
    val = abs(val)

    if decimals > 0:
        val_rounded = round(val, decimals)
        dec_part = f"{val_rounded:.{decimals}f}".split(".")[1]
        int_part = int(val_rounded)
    else:
        int_part = int(round(val))
        dec_part = None

    s = str(int_part)
    if len(s) <= 3:
        formatted_int = s
    else:
        # Last 3 digits
        last3 = s[-3:]
        remaining = s[:-3]
        # Group remaining into 2s from right to left
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ",".join(groups) + "," + last3

    result = formatted_int
    if dec_part is not None:
        result += f".{dec_part}"

    if is_negative:
        if include_symbol:
            return f"-₹{result}"
        return f"-{result}"

    if include_symbol:
        return f"₹{result}"
    return result


def format_inr_compact(amount: float, include_symbol: bool = True) -> str:
    """
    Compact notation for large numbers:
    >= 1 Crore (1,00,00,000) -> ₹X.XX Cr
    >= 1 Lakh (1,00,000) -> ₹X.XX L
    >= 1 Thousand (1,000) -> ₹X.XX K
    """
    if amount is None:
        return "₹0" if include_symbol else "0"
    
    try:
        val = float(amount)
    except (ValueError, TypeError):
        return str(amount)

    prefix = "₹" if include_symbol else ""
    sign = "-" if val < 0 else ""
    val = abs(val)

    if val >= 10_000_000:
        cr = val / 10_000_000
        return f"{sign}{prefix}{cr:.2f} Cr"
    elif val >= 100_000:
        lakh = val / 100_000
        return f"{sign}{prefix}{lakh:.2f} L"
    elif val >= 1_000:
        k = val / 1_000
        return f"{sign}{prefix}{k:.1f} K"
    else:
        return f"{sign}{prefix}{val:,.0f}"


def format_percent(val: float, decimals: int = 2) -> str:
    """Format float as percentage: 8.5 -> '8.50%'"""
    if val is None:
        return "0.00%"
    return f"{float(val):.{decimals}f}%"


def format_tenure_display(months: int) -> str:
    """Convert tenure in months to 'X yrs Y mos' format"""
    years = months // 12
    rem_months = months % 12
    if years > 0 and rem_months > 0:
        return f"{years} yrs {rem_months} mos"
    elif years > 0:
        return f"{years} years" if years > 1 else "1 year"
    else:
        return f"{rem_months} months"
