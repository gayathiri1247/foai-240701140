def calculate_emi(principal, annual_rate_percent, tenure_months):
    """Reducing-balance EMI. Rate is annual percent; output is monthly payment."""
    p = float(principal)
    annual = float(annual_rate_percent)
    n = int(tenure_months)
    if p <= 0 or annual < 0 or n <= 0:
        raise ValueError("Principal and tenure must be positive; rate cannot be negative.")
    r = annual / 1200.0
    if r == 0:
        return p / n
    factor = (1 + r) ** n
    return p * r * factor / (factor - 1)
