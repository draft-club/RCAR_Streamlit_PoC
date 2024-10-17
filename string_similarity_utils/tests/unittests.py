import unittest
from column_standarizer.levenstein import LevenshteinDistance

class TestLevenshteinDistance(unittest.TestCase):
    def setUp(self):
        """Set up necessary objects before running tests."""
        self.distance = LevenshteinDistance()

    def test_calculate_same_string(self):
        """Test that Levenshtein distance for identical strings is 0."""
        self.assertEqual(self.distance.calculate('اسم العميل', 'اسم العميل'), 0)

    def test_calculate_different_strings(self):
        """Test that Levenshtein distance for different strings is greater than 0."""
        self.assertGreater(self.distance.calculate('اسم العميل', 'العميل'), 0)

    def test_standardize(self):
        """Test standardization of input columns against reference columns."""
        input_columns = ['اسم العميل']
        standardized_cols = self.distance.standardize(input_columns)
        self.assertEqual(standardized_cols, ['اسم العميل'])  # Assuming 'اسم العميل' is in the reference

if __name__ == '__main__':
    unittest.main()