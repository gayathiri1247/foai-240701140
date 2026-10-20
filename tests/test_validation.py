import unittest
from backend.validation import validate

class ValidationTests(unittest.TestCase):
    def test_missing_required(self):
        errors = validate("personal", {})
        self.assertTrue(errors)
    def test_negative_income(self):
        data = {"age": 30, "employment_sector": "Corporate", "salary_account": "yes",
                "service_years": 2, "monthly_income": -1, "existing_emi": 0,
                "requested_amount": 10000, "tenure_months": 12}
        self.assertTrue(any("negative" in e.lower() for e in validate("personal", data)))
    def test_unsupported_loan(self):
        self.assertTrue(validate("unknown", {}))

if __name__ == "__main__":
    unittest.main()
