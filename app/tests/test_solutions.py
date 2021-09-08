import unittest

from app import solutions


class SolutionUtilitiesTests(unittest.TestCase):

    def setUp(self):
        self.attempt = {
            "question": "2 x + 3 = 0",
            "attempt": "x = - \\frac{3}{2}"
        }

    def test_check_solution_valid(self):

        question_type = "mcat"
        question_id = "1"

        response, status = solutions.check_solution(question_type, question_id, self.attempt)

        self.assertEqual(200, status)
        self.assertEqual(self.attempt.get("question"), response.json.get("question"))
        self.assertEqual(self.attempt.get("attempt"), response.json.get("attempt"))
        self.assertEqual(True, response.json.get("result"))


    def test_check_solution_invalid_id(self):

        question_type = "mcat"
        question_id = "999"

        response, status = solutions.check_solution(question_type, question_id, self.attempt)

        self.assertEqual(404, status)
        self.assertIsInstance(response, solutions.AttemptError)
        self.assertEqual("Solution or question not found.", response.json.get("description"))

    def test_check_solution_invalid_type(self):

        question_type = "batman"
        question_id = "999"

        response, status = solutions.check_solution(question_type, question_id, self.attempt)

        self.assertEqual(404, status)
        self.assertIsInstance(response, solutions.AttemptError)
        self.assertEqual("Solution or question not found.", response.json.get("description"))
