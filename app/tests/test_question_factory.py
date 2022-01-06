# pylint: disable=C0103
import unittest

import app.api.models.questions_mcat


class QuestionsTests(unittest.TestCase):

    def test_MCAT_Question_1(self):
        seed = 123
        question = app.api.models.questions_mcat.MCATQuestion1(seed)

        self.assertEqual("Solve a linear equation.", question.description)
        self.assertEqual("5 x + 7 = 0", question.question)
        self.assertEqual(seed, question.seed)
        self.assertTrue("description" in question.json.keys())
        self.assertTrue("question" in question.json.keys())

    def test_MCAT_Question_2(self):
        seed = 123
        question = app.api.models.questions_mcat.MCATQuestion2(seed)

        self.assertEqual("Adding like terms.", question.description)
        question.validate_attempt("a")
