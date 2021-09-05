import unittest
from app import maths_service


class MathsServiceTests(unittest.TestCase):

    def test_integer_coefficients_same_seed(self):
        seed = 2000
        coefficients_1 = maths_service.integer_coefficients(amount=3, seed=seed)
        coefficients_2 = maths_service.integer_coefficients(amount=3, seed=seed)

        self.assertEqual(coefficients_1, coefficients_2)
        self.assertEqual(3, len(coefficients_1))
        
        for integer in coefficients_1:
            self.assertIsInstance(integer, int)


if __name__ == "__main__":
    unittest.main()