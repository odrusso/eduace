import unittest

import app.api.services.solution_service
from app.api.helpers.errors import HttpError


class SolutionUtilitiesTests(unittest.TestCase):

    def setUp(self):
        self.attempt = {
            "question": "2 x + 3 = 0",
            "attempt": "x = - \\frac{3}{2}"
        }

    def test_check_solution_valid(self):

        question_type = "mcat"
        question_id = "1"

        response, status = app.api.services.solution_service.check_solution(question_type,
                                                                            question_id,
                                                                            self.attempt)

        self.assertEqual(200, status)
        self.assertEqual(self.attempt.get("question"), response.json.get("question"))
        self.assertEqual(self.attempt.get("attempt"), response.json.get("attempt"))
        self.assertEqual(True, response.json.get("result"))

    def test_check_solution_invalid_id(self):

        question_type = "mcat"
        question_id = "999"

        try:
            response, status = app.api.services.solution_service.check_solution(question_type,
                                                                                question_id,
                                                                                self.attempt)

        except HttpError as error:
            response = error
            status = error.json.get("status")

        self.assertEqual(404, status)
        self.assertIsInstance(response, HttpError)
        self.assertEqual("Question mcat 999 not found.", response.json.get("description"))

    def test_check_solution_invalid_type(self):

        question_type = "batman"
        question_id = "999"

        try:
            response, status = app.api.services.solution_service.check_solution(question_type,
                                                                                question_id,
                                                                                self.attempt)

        except HttpError as error:
            response = error
            status = error.json.get("status")

        self.assertEqual(404, status)
        self.assertIsInstance(response, HttpError)
        self.assertEqual("Question batman 999 not found.", response.json.get("description"))
