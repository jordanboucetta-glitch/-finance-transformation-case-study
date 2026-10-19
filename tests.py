import unittest
from finance_pipeline import generate_data, analyze

class FinanceTests(unittest.TestCase):
    def test_rows(self):
        self.assertEqual(len(generate_data()), 12 * 5 * 5)

    def test_reproducible(self):
        self.assertTrue(generate_data().equals(generate_data()))

    def test_variances(self):
        df = analyze(generate_data())
        self.assertTrue(((df.actual_eur - df.budget_eur - df.variance_eur).abs() < .011).all())

    def test_no_missing_or_duplicates(self):
        df = analyze(generate_data())
        self.assertFalse(df.isna().any().any())
        self.assertFalse(df.duplicated(["month", "department", "category"]).any())

if __name__ == "__main__":
    unittest.main()
