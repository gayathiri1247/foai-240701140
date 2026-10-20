import unittest
from backend.inference_engine import evaluate_application

class InferenceTests(unittest.TestCase):
    def test_each_loan_type_returns_incomplete_for_unverified_policy(self):
        cases = {
            "personal": {"age": 30, "employment_sector": "Corporate", "salary_account": "yes", "service_years": 2, "monthly_income": 50000, "existing_emi": 0, "requested_amount": 100000, "tenure_months": 24},
            "home": {"age": 30, "employment_type": "Salaried", "monthly_income": 50000, "existing_emi": 0, "property_value": 4000000, "requested_amount": 2500000, "down_payment": 1500000, "tenure_months": 240},
            "car": {"age": 30, "applicant_category": "Salaried", "annual_income": 600000, "existing_emi": 0, "vehicle_price": 1000000, "requested_amount": 800000, "tenure_months": 60},
            "education": {"nationality": "Indian", "course": "Engineering", "institution": "College", "study_location": "India", "admission_status": "yes", "course_expenses": 500000, "requested_amount": 400000, "co_borrower": "yes", "tenure_months": 120},
        }
        for loan_type, data in cases.items():
            result = evaluate_application(loan_type, data)
            self.assertEqual(result["decision"], "Incomplete")
            self.assertTrue(result["rule_results"])
    def test_missing_data_is_incomplete(self):
        result = evaluate_application("home", {})
        self.assertEqual(result["decision"], "Incomplete")

if __name__ == "__main__":
    unittest.main()
