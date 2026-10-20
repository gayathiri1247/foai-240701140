from backend.loan_rules import RULES, LOANS
from backend.validation import validate
from backend.explanation import make_summary


def _result(rule, passed=None, explanation=None):
    status = "Not Evaluated" if passed is None else ("Pass" if passed else "Fail")
    return {"rule_id": rule["rule_id"], "status": status,
            "explanation": explanation or rule["condition"],
            "verification_status": rule["verification_status"],
            "source_url": rule["source_url"]}


def _number(data, key):
    try:
        return float(data.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _evaluate_personal(data, rules):
    sector = str(data.get("employment_sector", "")).strip().lower()
    government = sector in {"central government", "state government", "railway", "police", "psu"}
    defence = sector in {"defence", "defense", "central armed police", "coast guard"}
    corporate = sector == "corporate"
    eligible_group = government or defence or corporate
    salary_min = 20000 if government or defence else 25000
    service_min_months = 12 if corporate else 6
    age = int(_number(data, "age"))
    amount = _number(data, "requested_amount")
    months = int(_number(data, "tenure_months"))
    income = _number(data, "monthly_income")
    existing_emi = _number(data, "existing_emi")
    rules_by_id = {r["rule_id"]: r for r in rules}
    salary_and_group = (eligible_group and data.get("salary_account", "").lower() == "yes"
                        and data.get("nationality", "").lower() == "indian")
    service_and_salary = (eligible_group and income >= salary_min
                          and _number(data, "service_years") * 12 >= service_min_months)
    basic_age_amount_tenure = (age >= 21 and amount >= 100000 and amount <= 5000000
                               and 6 <= months <= 84)
    if age <= 60:
        age_result = basic_age_amount_tenure
    elif age > 60 and (government or defence):
        age_result = None  # SBI permits case-by-case consideration.
    else:
        age_result = False
    retirement_months = _number(data, "months_to_retirement")
    closure_limit = min(retirement_months, max(0, (60 - age) * 12))
    closure_result = months <= closure_limit if age <= 60 else (None if government or defence else False)
    amount_cap = min(5000000, 30 * income)
    headroom = 0.65 * income - existing_emi
    return [
        _result(rules_by_id["PL-01"], salary_and_group,
                "Indian nationality, eligible employee sector, and SBI salary-package account checked."),
        _result(rules_by_id["PL-02"], service_and_salary,
                f"Requires {service_min_months} months of service and net monthly salary of at least ₹{salary_min:,.0f} for this employee group."),
        _result(rules_by_id["PL-03"], age_result,
                "SBI publishes age 21–60, with government/defence applicants above 60 considered case by case; amount and tenure limits also checked."),
        _result(rules_by_id["PL-04"], 100000 <= amount <= amount_cap,
                f"Requested amount ₹{amount:,.0f}; maximum from the published 30× NMI and ₹50 lakh caps is ₹{amount_cap:,.0f}."),
        _result(rules_by_id["PL-07"],
                closure_result,
                f"Requested {months} months; entered months to retirement/end of contract: {retirement_months:g}. SBI requires closure by retirement/end of contract/age 60, as applicable."),
        _result(rules_by_id["PL-05"], None,
                f"Existing EMI ₹{existing_emi:,.0f}; at 65% EMI/NMI, the maximum room for the new EMI is ₹{max(0, headroom):,.0f}/month. Cannot decide without SBI's actual offered EMI and rate."),
        _result(rules_by_id["PL-06"], None,
                "Credit score and SBI internal credit policy cannot be checked by this application."),
    ]


def _evaluate_home(data, rules):
    age = int(_number(data, "age"))
    months = int(_number(data, "tenure_months"))
    amount = _number(data, "requested_amount")
    property_value = _number(data, "property_value")
    rules_by_id = {r["rule_id"]: r for r in rules}
    ratio = 0.90 if amount <= 2000000 else (0.80 if amount <= 7500000 else 0.75)
    ltv_limit = property_value * ratio
    return [
        _result(rules_by_id["HL-01"], data.get("resident_status", "").lower() == "resident indian"
                and age >= 18 and age + months / 12 <= 70 and months <= 360,
                "Resident status, age at loan maturity (≤70) and tenure (≤30 years) checked."),
        _result(rules_by_id["HL-02"], amount <= ltv_limit,
                f"For a requested amount of ₹{amount:,.0f}, the published LTV tier permits at most {ratio:.0%} of property value: ₹{ltv_limit:,.0f}, using the value entered. SBI must use its assessed value."),
        _result(rules_by_id["HL-03"], None,
                "SBI must verify assessed property value, title/legal documents, credit history and repayment capacity."),
    ]


def _evaluate_car(data, rules):
    category = data.get("applicant_category", "").lower()
    applicant = _number(data, "annual_income")
    co_applicant = _number(data, "co_applicant_annual_income")
    combined_income = applicant + co_applicant
    age = int(_number(data, "age"))
    months = int(_number(data, "tenure_months"))
    amount = _number(data, "requested_amount")
    if category == "public/defence salary package":
        min_income, max_amount = 300000, combined_income * 4
    elif category == "self-employed / business / professional":
        min_income, max_amount = 300000, combined_income * 4
    elif category == "agriculture / allied activities":
        min_income, max_amount = 400000, combined_income * 3
    else:
        min_income, max_amount = float("inf"), 0
    income_ok = combined_income >= min_income and amount <= max_amount
    return [
        _result(rules[0], 21 <= age <= 70, "SBI new-car applicant age is 21–70 years."),
        _result(rules[1], income_ok,
                f"Combined entered annual qualifying income ₹{combined_income:,.0f}; category minimum ₹{min_income:,.0f}; formula cap ₹{max_amount:,.0f}. SBI must verify the income basis and any co-applicant."),
        _result(rules[2], 1 <= months <= 84, "SBI new-car loan repayment tenure is up to 7 years."),
        _result(rules[3], None,
                "SBI verifies income proofs, vehicle on-road price, borrower/co-applicant details and creditworthiness."),
        _result(rules[4], amount <= _number(data, "vehicle_price"),
                f"Requested amount ₹{amount:,.0f}; entered on-road price ₹{_number(data, 'vehicle_price'):,.0f}. SBI publishes financing up to 100% of on-road price."),
    ]


def _evaluate_education(data, rules):
    location = data.get("study_location", "").lower()
    course = data.get("course_category", "").lower()
    top = data.get("institution_category", "").lower() == "top 100 nirf (applicant declared)"
    admission = data.get("admission_status", "").lower() == "yes"
    amount = _number(data, "requested_amount")
    expenses = _number(data, "course_expenses")
    months = int(_number(data, "tenure_months"))
    indian = data.get("nationality", "").lower() == "indian"
    if location == "india":
        medical = course == "medical (mbbs/md/ms)"
        limit = (7500000 if medical else 5000000) if top else (5000000 if medical else 3000000)
        exceptional_limit = 10000000 if (medical or top) else 5000000
        margin = 0 if amount <= 400000 else 0.05
    else:
        limit = 750000  # Higher overseas limits are a separate SBI Global Ed-vantage product.
        exceptional_limit = limit
        margin = 0 if amount <= 400000 else 0.15
    finance_limit = expenses * (1 - margin)
    parent_or_guardian = data.get("co_borrower", "").lower() == "yes" and data.get("co_borrower_relation", "").lower() in {"parent", "guardian"}
    collateral = data.get("collateral_available", "").lower()
    co_borrower_answer = data.get("co_borrower", "").lower()
    if co_borrower_answer == "no" or (co_borrower_answer == "yes" and not parent_or_guardian):
        security_result = False
    elif co_borrower_answer == "unknown" or (amount > 7500000 and collateral == "unknown"):
        security_result = None
    else:
        security_result = parent_or_guardian and (amount <= 7500000 or collateral == "yes")
    if amount <= limit:
        amount_result = amount <= finance_limit
    elif amount <= exceptional_limit:
        amount_result = None if amount <= finance_limit else False
    else:
        amount_result = False
    rules_by_id = {r["rule_id"]: r for r in rules}
    return [
        _result(rules_by_id["EL-01"], indian and admission,
                "Indian nationality and secured admission checked. SBI must verify that the course and institution meet its published eligibility list."),
        _result(rules_by_id["EL-02"], amount_result,
                f"Requested ₹{amount:,.0f}; standard cap ₹{limit:,.0f}; SBI may consider up to ₹{exceptional_limit:,.0f} case by case in India; margin-adjusted course expenses support ₹{finance_limit:,.0f}."),
        _result(rules_by_id["EL-03"], 1 <= months <= 180,
                "Requested repayment period checked against up to 15 years after course/moratorium."),
        _result(rules_by_id["EL-04"], security_result,
                "Parent/guardian co-borrower required; tangible collateral is also required for requests above ₹7.5 lakh."),
        _result(rules_by_id["EL-05"], None,
                "SBI must verify course admission, institution status, income documents, collateral value and security acceptability."),
    ]


def evaluate_application(loan_type, data):
    errors = validate(loan_type, data)
    if errors:
        results = [{"rule_id": f"INPUT-{i:02d}", "status": "Fail", "explanation": error,
                    "verification_status": "Input validation", "source_url": LOANS[loan_type]["source"]}
                   for i, error in enumerate(errors, 1)]
        return {"decision": "Incomplete", "summary": "Please correct the form errors before assessment.", "rule_results": results}

    applicable = [rule for rule in RULES if rule["loan_type"] == loan_type]
    evaluators = {"personal": _evaluate_personal, "home": _evaluate_home,
                  "car": _evaluate_car, "education": _evaluate_education}
    results = evaluators[loan_type](data, applicable)
    if any(row["status"] == "Fail" for row in results):
        decision = "Ineligible under configured rules"
    elif any(row["status"] == "Not Evaluated" for row in results):
        decision = "Incomplete — bank checks remain"
    else:
        decision = "Passed configured checks — bank review required"
    return {"decision": decision, "summary": make_summary(decision, results), "rule_results": results}
