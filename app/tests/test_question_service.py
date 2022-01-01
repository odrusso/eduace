import unittest

from app.api.services import question_service


class QuestionUtilitiesTests(unittest.TestCase):

    def test_get_question_success(self):
        question_type = "mcat"
        question_id = "1"
        seed = 123

        question = question_service.get_question(question_type, question_id, seed)

        self.assertEqual("Solve a linear equation.", question.description)
        self.assertEqual("5 x + 7 = 0", question.question)

    def test_get_questions_throws_error_with_nonexistant_input(self):
        question_type = "mcat"
        question_id = "99"
        seed = 123

        question = None

        try:
            question = question_service.get_question(question_type, question_id, seed)
        except Exception as exception: # pylint: disable=W0703
            self.assertIsInstance(exception, TypeError)

        self.assertIsNone(question)

    def test_get_all_questions(self):

        response = question_service.get_all_questions()

        self.assertTrue("questions" in response.keys())

        all_questions = response.get("questions")

        self.assertTrue(len(all_questions) > 0)

        for question_type in question_service.QUESTION_MAPPING.keys(): # pylint: disable=consider-iterating-dictionary
            question_types = [question.get("questionTypeName") for question in all_questions]
            self.assertTrue(question_type in question_types)
