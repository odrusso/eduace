import unittest
from app.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_question(self):
        response = self.client.get("/api/v1/question/mcat/1?seed=123")

        status = response.status
        data = response.get_json()

        self.assertEqual('200 OK', status)
        self.assertTrue("description" in data.keys())
        self.assertTrue("question" in data.keys())

    def test_get_question_not_found(self):
        response = self.client.get("/api/v1/question/mcat/99?seed=123")

        status = response.status
        data = response.get_json()

        self.assertEqual('404 NOT FOUND', status)
        self.assertTrue("Question not found." in data.get("description"))

    def test_get_question_type_not_found(self):
        response = self.client.get("/api/v1/question/bob/1?seed=123")

        status = response.status
        data = response.get_json()

        self.assertEqual('404 NOT FOUND', status)
        self.assertTrue("Question type not found." in data.get("description"))

    def test_get_all_questions(self):
        response = self.client.get("/api/v1/questions")

        status = response.status
        data = response.get_json()

        self.assertEqual('200 OK', status)
        self.assertTrue("questions" in data.keys())
        self.assertTrue(len(data.get("questions")) > 0)
