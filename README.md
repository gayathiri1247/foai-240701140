# SBI Multi-Loan Eligibility Checker

A local educational college project built with Flask, SQLite, HTML, CSS, JavaScript and Bootstrap 5. It includes registration/login, loan selection, loan-specific forms, a rule-based assessment workflow, saved history, and a policy-source page.

## Run on Windows

1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Open Terminal and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:5000

Register a demo account and try a loan form. The database is created automatically in `database/sbi_demo.sqlite3`.

## Run tests

```powershell
.venv\Scripts\activate
python -m unittest discover -s tests -v
```

## Policy assessment limits

The evaluator applies published SBI criteria for the configured personal, home, new-car and Student Loan Scheme products. A failed configured criterion is shown as ineligible under that rule. A passing result is only a pre-screen: credit history, documents, institution/property verification, actual repayment capacity and SBI underwriting still require bank review. Some inputs (for example income and institution category) are applicant-declared and are not independently verified by this local demo.

Official starting sources:
- Personal loan: https://sbi.bank.in/web/personal-banking/loans/personal-loans/sbi-personal-loan
- Home loan: https://sbi.bank.in/web/personal-banking/loans/home-loans
- New car loan: https://sbi.bank.in/web/personal-banking/loans/auto-loans/sbi-new-car-loan-scheme
- Education loan: https://sbi.bank.in/web/personal-banking/loans/education-loans/student-loan-scheme

## Demo security notes

Passwords are hashed and records are scoped to the logged-in demo account. This is a college prototype, not production banking software. Before deployment, set a strong `FLASK_SECRET_KEY`, use HTTPS, add CSRF protection and security review, and verify the policy rules.

## Reset local demo data

Stop the server and delete `database/sbi_demo.sqlite3`. The app recreates an empty database at next startup.
