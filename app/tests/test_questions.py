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

    def test_get_question_failure_type(self):
        question_type = "bob"
        question_id = "1"
        seed = 123

        question, status = questions.get_question(question_type, question_id, seed)

        self.assertEqual("Question type not found.", question.description)
        self.assertEqual(404, status)

    def test_get_question_failure_id(self):
        question_type = "mcat"
        question_id = "99"
        seed = 123

        question, status = questions.get_question(question_type, question_id, seed)

        self.assertEqual("Question not found.", question.description)
        self.assertEqual(404, status)

    def test_get_all_questions(self):

        response, status = questions.get_all_questions()

        self.assertTrue("questions" in response.keys())
        self.assertEqual(200, status)

        for question_type in questions.QUESTION_MAPPING.keys():
            self.assertTrue(question_type in [question.get("questionTypeName") for question in response.get("questions")])


class QuestionsTests(unittest.TestCase):

    def test_MCAT_Question_1(self):
        seed = 123
        question = questions.MCATQuestion1(seed)

        self.assertEqual("Solve a linear equation.", question.description)
        self.assertEqual("5 x + 7 = 0", question.question)
        self.assertEqual(seed, question.seed)
        self.assertTrue("description" in question.json.keys())
        self.assertTrue("question" in question.json.keys())
