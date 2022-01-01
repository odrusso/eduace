import unittest

from app.api.services import solution_service


class SolutionUtilitiesTests(unittest.TestCase):
    def test_check_solution_valid(self):

        question_type = "mcat"
        question_id = "1"

        response = solution_service.check_solution(question_type, question_id,
                                                   "x = - \\frac{1}{2}", 1)

        self.assertEqual(True, response)

    def test_check_solution_not_simplified_enough(self):

        question_type = "mcat"
        question_id = "1"

        response = solution_service.check_solution(question_type, question_id,
                                                   "x = - \\frac{5}{10}", 1)

        # self.assertTrue(response)
        # this may not be the behaviour that we want.
        self.assertTrue(response)

    def test_check_solution_invalid(self):

        question_type = "mcat"
        question_id = "1"

        response = solution_service.check_solution(question_type, question_id,
                                                   "x = - \\frac{2}{2}", 1)

        self.assertFalse(response)
