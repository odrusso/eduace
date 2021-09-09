import unittest

from app import questions


class QuestionUtilitiesTests(unittest.TestCase):

    def test_get_question_success(self):
        question_type = "mcat"
        question_id = "1"
        seed = 123

        question, status = questions.get_question(question_type, question_id, seed)

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
            question, status = questions.get_question(question_type, question_id, seed)
        except questions.QuestionNotFound as not_found:
            self.assertEqual("Question not found.", not_found.json.get("description"))

        self.assertIsNone(question)
        self.assertIsNone(status)

    def test_get_all_questions(self):

        response, status = questions.get_all_questions()

        self.assertTrue("questions" in response.keys())
        self.assertEqual(200, status)

        all_questions = response.get("questions")

        self.assertTrue(len(all_questions) > 0)

        for question_type in questions.QUESTION_MAPPING.keys(): # pylint: disable=consider-iterating-dictionary
            question_types = [question.get("questionTypeName") for question in all_questions]
            self.assertTrue(question_type in question_types)
