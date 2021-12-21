import unittest

from app.api.services import solution_service


class SolutionServiceTests(unittest.TestCase):

    # The following tests will need to be improved as is_correct
    # grows in complexity

    def test_is_correct_correct(self):

        question = "2 x + 3 = 0"
        attempt = "x = -\\frac{3}{2}"

        result = solution_service.is_correct(question, attempt)

        self.assertTrue(result)

    def test_is_correct_incorrect(self):

        question = "2 x + 3 = 0"
        attempt = "x = 1000"

        result = solution_service.is_correct(question, attempt)

        self.assertFalse(result)

    def test_is_correct_repeat_question(self):

        question = "2 x + 3 = 0"
        attempt = "2 x + 3 = 0"

        result = solution_service.is_correct(question, attempt)

        self.assertFalse(result)
