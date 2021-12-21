import json
import unittest

from app.api import app


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
        self.assertTrue("Question not found." in data.get("description"))

    def test_get_all_questions(self):
        response = self.client.get("/api/v1/questions")

        status = response.status
        data = response.get_json()

        self.assertEqual('200 OK', status)
        self.assertTrue("questions" in data.keys())
        self.assertTrue(len(data.get("questions")) > 0)

    def test_check_solution_correct(self):
        body = {"question": "2 x + 3 = 0", "attempt": "x = -\\frac{3}{2}"}
        response = self.client.post("/api/v1/question/mcat/1",
                                    data=json.dumps(body),
                                    content_type='application/json')

        status = response.status
        data = response.get_json()

        self.assertEqual("200 OK", status)
        self.assertEqual(body.get("question"), data.get("question"))
        self.assertEqual(body.get("attempt"), data.get("attempt"))
        self.assertEqual(True, data.get("result"))

    def test_check_solution_incorrect(self):
        body = {"question": "2 x + 3 = 0", "attempt": "x = 1000"}

        response = self.client.post("/api/v1/question/mcat/1",
                                    data=json.dumps(body),
                                    content_type='application/json')

        status = response.status
        data = response.get_json()

        self.assertEqual("200 OK", status)
        self.assertEqual(body.get("question"), data.get("question"))
        self.assertEqual(body.get("attempt"), data.get("attempt"))
        self.assertEqual(False, data.get("result"))
