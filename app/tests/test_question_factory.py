# pylint: disable=C0103
import unittest
from app import question_factory


class QuestionsTests(unittest.TestCase):

    def test_MCAT_Question_1(self):
        seed = 123
        question = question_factory.MCATQuestion1(seed)

        self.assertEqual("Solve a linear equation.", question.description)
        self.assertEqual("5 x + 7 = 0", question.question)
        self.assertEqual(seed, question.seed)
        self.assertTrue("description" in question.json.keys())
        self.assertTrue("question" in question.json.keys())
