import unittest

from app import maths_service


class MathsServiceTests(unittest.TestCase):

    def test_integer_coefficients_same_seed(self):
        seed = 2000
        expectation = [-1, -5, 10]

        coefficients_1 = maths_service.integer_coefficients(amount=3, seed=seed)
        coefficients_2 = maths_service.integer_coefficients(amount=3, seed=seed)

        self.assertEqual(expectation, coefficients_1)
        self.assertEqual(expectation, coefficients_2)
        self.assertEqual(3, len(coefficients_1))
        
        for integer in coefficients_1:
            self.assertIsInstance(integer, int)

    def test_integer_coefficients_different_seed(self):
        seed_1 = 2000
        seed_2 = 2999

        coefficients_1 = maths_service.integer_coefficients(amount=3, seed=seed_1)
        coefficients_2 = maths_service.integer_coefficients(amount=3, seed=seed_2)

        self.assertNotEqual(coefficients_1, coefficients_2)
        self.assertEqual(3, len(coefficients_1))
        
        for integer in coefficients_1:
            self.assertIsInstance(integer, int)


if __name__ == "__main__":
    unittest.main()
