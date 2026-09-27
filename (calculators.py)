import numpy as np

def validate_positive_inputs(**kwargs):
    for key, value in kwargs.items():
        if value is None or value < 0:
            raise ValueError(f"Invalid input for '{key}': Positive number required.")

def calculate_sip(monthly_investment: float, annual_rate: float, tenure_years: int):
    validate_positive_inputs(monthly_investment=monthly_investment, annual_rate=annual_rate, tenure_years=tenure_years)
    if tenure_years == 0:
        raise ValueError("Tenure must be at least 1 year.")
    n = int(tenure_years * 12)
    i = annual_rate / 12 / 100
    months = np.arange(1, n + 1)
    if i == 0:
        invested_series = monthly_investment * months
        wealth_series = invested_series.copy()
    else:
        invested_series = monthly_investment * months
        wealth_series = monthly_investment * (((1 + i) ** months - 1) / i) * (1 + i)
    total_invested = invested_series[-1]
    maturity_value = wealth_series[-1]
    estimated_returns = maturity_value - total_invested
    return {
        "total_invested": round(float(total_invested), 2),
        "estimated_returns": round(float(estimated_returns), 2),
        "maturity_value": round(float(maturity_value), 2),
        "months": months,
        "invested_series": invested_series,
        "wealth_series": wealth_series
    }

def calculate_emi(principal: float, annual_rate: float, tenure_years: int):
    validate_positive_inputs(principal=principal, annual_rate=annual_rate, tenure_years=tenure_years)
    if tenure_years == 0 or principal == 0:
        raise ValueError("Principal and Tenure must be greater than zero.")
    n = int(tenure_years * 12)
    r = annual_rate / 12 / 100
    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    total_payment = emi * n
    total_interest = total_payment - principal
    return {
        "monthly_emi": round(float(emi), 2),
        "total_interest": round(float(total_interest), 2),
        "total_payment": round(float(total_payment), 2)
    }

def calculate_compound_interest(principal: float, annual_rate: float, tenure_years: float, frequency: int = 12):
    validate_positive_inputs(principal=principal, annual_rate=annual_rate, tenure_years=tenure_years)
    r = annual_rate / 100
    amount = principal * (1 + r / frequency) ** (frequency * tenure_years)
    interest_earned = amount - principal
    years = np.arange(1, int(tenure_years) + 1)
    yearly_amounts = principal * (1 + r / frequency) ** (frequency * years)
    return {
        "principal": round(float(principal), 2),
        "interest_earned": round(float(interest_earned), 2),
        "final_amount": round(float(amount), 2),
        "years": years,
        "yearly_amounts": yearly_amounts
    }

def compare_loans(loan_amount: float, rate_1: float, tenure_1: int, rate_2: float, tenure_2: int):
    opt1 = calculate_emi(loan_amount, rate_1, tenure_1)
    opt2 = calculate_emi(loan_amount, rate_2, tenure_2)
    return {"Option 1": opt1, "Option 2": opt2}
