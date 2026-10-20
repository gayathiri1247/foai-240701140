import unittest
from backend.calculations import calculate_emi

class CalculationTests(unittest.TestCase):
    def test_positive_rate(self):
        self.assertAlmostEqual(calculate_emi(120000, 12, 12), 10661.85, delta=1)
    def test_zero_rate(self):
        self.assertEqual(calculate_emi(12000, 0, 12), 1000)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            calculate_emi(0, 5, 12)

if __name__ == "__main__":
    unittest.main()
