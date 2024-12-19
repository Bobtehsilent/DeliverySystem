import unittest
from src.data_processing import load_data, validate_data


class TestDataProcessing(unittest.TestCase):
    def test_load_data(self):
        df = load_data('data/lagerstatus.csv')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    def test_validate_data(self):
        df = load_data('data/lagerstatus.csv')
        valid, _ = validate_data(df)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()