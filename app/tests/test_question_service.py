import unittest

from app.api.services import question_service
from app.api.helpers.errors import HttpError


class QuestionUtilitiesTests(unittest.TestCase):

    def test_get_question_success(self):
        question_type = "mcat"
        question_id = "1"
        seed = 123

        question, status = question_service.get_question(question_type, question_id, seed)

        self.assertEqual("Solve a linear equation.", question.description)
        self.assertEqual("5 x + 7 = 0", question.question)
        self.assertEqual(200, status)

    def test_get_question_failure(self):
        question_type = "mcat"
        question_id = "99"
        seed = 123

        question = None
        status = None

        try:
            question, status = question_service.get_question(question_type, question_id, seed)
        except HttpError as not_found:
            self.assertEqual("Question not found.", not_found.json.get("description"))

        self.assertIsNone(question)
        self.assertIsNone(status)

    def test_get_all_questions(self):

        response, status = question_service.get_all_questions()

        self.assertTrue("questions" in response.keys())
        self.assertEqual(200, status)

        all_questions = response.get("questions")

        self.assertTrue(len(all_questions) > 0)

        for question_type in question_service.QUESTION_MAPPING.keys(): # pylint: disable=consider-iterating-dictionary
            question_types = [question.get("questionTypeName") for question in all_questions]
            self.assertTrue(question_type in question_types)
