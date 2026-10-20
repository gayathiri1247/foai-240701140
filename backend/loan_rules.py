"""SBI scheme criteria used by the pre-screening evaluator.

Criteria below are transcribed from the linked SBI product pages. SBI's final
credit decision also depends on documents, credit checks and bank discretion.
Review the source pages regularly because product terms can change.
"""
SOURCES = {
    "personal": "https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan",
    "home": "https://sbi.bank.in/web/yono/home-loan",
    "car": "https://sbi.bank.in/web/personal-banking/loans/auto-loans/sbi-new-car-loan-scheme",
    "education": "https://sbi.bank.in/web/personal-banking/loans/education-loans/student-loan-scheme",
}

LOANS = {
    "personal": {"name": "Personal Loan", "description": "Pre-screen a personal-loan application.", "source": SOURCES["personal"]},
    "home": {"name": "Home Loan", "description": "Pre-screen a home-loan application.", "source": SOURCES["home"]},
    "car": {"name": "New Car Loan", "description": "Pre-screen a new-car loan application.", "source": SOURCES["car"]},
    "education": {"name": "Student Loan Scheme", "description": "Pre-screen an SBI student-loan application.", "source": SOURCES["education"]},
}

# The rules page renders these same criteria and their status/source.
RULES = [
    {"rule_id": "PL-01", "loan_type": "personal", "description": "Eligible employee group and SBI salary-package account", "condition": "Government, Defence or Corporate employee; SBI salary-package account required", "verification_status": "Implemented", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-02", "loan_type": "personal", "description": "Minimum service and net monthly salary", "condition": "Government/Defence: 6 months and ₹20,000; Corporate: 12 months and ₹25,000", "verification_status": "Implemented", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-03", "loan_type": "personal", "description": "Age, loan amount and tenure", "condition": "Age 21–60; ₹1–50 lakh; tenure 6–84 months", "verification_status": "Implemented", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-04", "loan_type": "personal", "description": "Maximum amount based on net monthly income", "condition": "Up to 30 times net monthly income", "verification_status": "Implemented", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-05", "loan_type": "personal", "description": "EMI to net monthly income ratio", "condition": "Total EMI/NMI ratio must not exceed 65%", "verification_status": "Requires SBI's actual offer and EMI assessment", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-06", "loan_type": "personal", "description": "Credit score and bank internal policy", "condition": "Satisfactory credit score under SBI's internal policy", "verification_status": "Bank-only check", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "PL-07", "loan_type": "personal", "description": "Close loan by retirement/end of contract/age 60", "condition": "Loan must close by retirement, contract end or age 60, as applicable", "verification_status": "Applicant-declared date; SBI must verify", "source_url": SOURCES["personal"], "last_checked": "2026-10-13"},
    {"rule_id": "HL-01", "loan_type": "home", "description": "Resident status, age at maturity and tenure", "condition": "Resident Indian; minimum age 18; age at loan maturity no more than 70; tenure up to 30 years", "verification_status": "Implemented", "source_url": SOURCES["home"], "last_checked": "2026-10-13"},
    {"rule_id": "HL-02", "loan_type": "home", "description": "Maximum loan-to-value ratio", "condition": "Up to 90% for loans ≤₹20 lakh; 80% above ₹20 lakh to ₹75 lakh; 75% above ₹75 lakh, based on assessed property value", "verification_status": "Pre-screened against applicant value; SBI valuation required", "source_url": "https://sbi.bank.in/webfiles/uploads/files/1356602766297_HOME_LOAN_MITC.pdf", "last_checked": "2026-10-13"},
    {"rule_id": "HL-03", "loan_type": "home", "description": "Property valuation, title and repayment-capacity checks", "condition": "SBI must verify valuation, legal title, credit and repayment capacity", "verification_status": "Bank-only check", "source_url": SOURCES["home"], "last_checked": "2026-10-13"},
    {"rule_id": "CL-01", "loan_type": "car", "description": "Applicant age", "condition": "Age 21–70 years", "verification_status": "Implemented", "source_url": SOURCES["car"], "last_checked": "2026-10-13"},
    {"rule_id": "CL-02", "loan_type": "car", "description": "Category income minimum and maximum amount", "condition": "Public/defence package: ₹3 lakh combined annual income and 48× monthly net income; self-employed: ₹3 lakh and 4× qualifying ITR income; agriculture: ₹4 lakh combined annual income and 3× annual income", "verification_status": "Implemented using applicant-entered income; SBI verifies proof", "source_url": SOURCES["car"], "last_checked": "2026-10-13"},
    {"rule_id": "CL-03", "loan_type": "car", "description": "Maximum repayment tenure", "condition": "Up to 7 years", "verification_status": "Implemented", "source_url": SOURCES["car"], "last_checked": "2026-10-13"},
    {"rule_id": "CL-04", "loan_type": "car", "description": "Income proof and creditworthiness", "condition": "SBI verifies income documents, co-applicant details, vehicle price and credit", "verification_status": "Bank-only check", "source_url": SOURCES["car"], "last_checked": "2026-10-13"},
    {"rule_id": "CL-05", "loan_type": "car", "description": "Vehicle financing limit", "condition": "Financing up to 100% of on-road price", "verification_status": "Implemented against applicant-entered price; SBI verifies quote", "source_url": SOURCES["car"], "last_checked": "2026-10-13"},
    {"rule_id": "EL-01", "loan_type": "education", "description": "Nationality and secured admission", "condition": "Indian national; admission secured for eligible higher-education course", "verification_status": "Partial; course/institution eligibility needs document review", "source_url": SOURCES["education"], "last_checked": "2026-10-13"},
    {"rule_id": "EL-02", "loan_type": "education", "description": "Loan limit and student contribution margin", "condition": "India: up to ₹75 lakh (medical) or ₹50 lakh (other) for Top 100 NIRF, otherwise ₹50 lakh/₹30 lakh; abroad: ₹7.5 lakh; above ₹4 lakh margin is 5% India or 15% abroad", "verification_status": "Implemented for standard Student Loan Scheme; institution status is applicant-declared", "source_url": SOURCES["education"], "last_checked": "2026-10-13"},
    {"rule_id": "EL-03", "loan_type": "education", "description": "Maximum repayment tenure", "condition": "Up to 15 years after course period and 12-month repayment holiday", "verification_status": "Implemented as a maximum of 180 months", "source_url": SOURCES["education"], "last_checked": "2026-10-13"},
    {"rule_id": "EL-04", "loan_type": "education", "description": "Co-borrower and collateral requirement", "condition": "Parent/guardian co-borrower required; above ₹7.5 lakh, tangible collateral security is required", "verification_status": "Implemented from published scheme terms", "source_url": SOURCES["education"], "last_checked": "2026-10-13"},
    {"rule_id": "EL-05", "loan_type": "education", "description": "Course, institution and security document verification", "condition": "SBI verifies eligibility documents and acceptable collateral/security", "verification_status": "Bank-only check", "source_url": SOURCES["education"], "last_checked": "2026-10-13"},
]

COMMON_REQUIRED = {
    "personal": ["age", "nationality", "employment_sector", "salary_account", "service_years", "months_to_retirement", "monthly_income", "existing_emi", "requested_amount", "tenure_months"],
    "home": ["age", "resident_status", "employment_type", "monthly_income", "existing_emi", "property_value", "requested_amount", "down_payment", "tenure_months"],
    "car": ["age", "applicant_category", "annual_income", "co_applicant_annual_income", "existing_emi", "vehicle_price", "requested_amount", "tenure_months"],
    "education": ["nationality", "course", "institution", "institution_category", "course_category", "study_location", "admission_status", "course_expenses", "requested_amount", "co_borrower", "co_borrower_relation", "collateral_available", "tenure_months"],
}

NUMERIC_FIELDS = {"age", "service_years", "months_to_retirement", "monthly_income", "annual_income", "co_applicant_annual_income", "existing_emi", "requested_amount", "property_value", "down_payment", "vehicle_price", "course_expenses", "tenure_months", "demo_annual_interest_rate"}
