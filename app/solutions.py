from .solution_service import is_correct
from .utils import is_question


class AttemptError(Exception):
    def __init__(self):
        self.description = "Solution or question not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class Attempt:
    def __init__(self, question, attempt, question_type, question_id, independent_var="x"):
        self.question_type = question_type
        self.question_id = question_id
        self.question = question
        self.attempt = attempt
        self.independent_var = independent_var

    @property
    def json(self):
        return {
            "question": self.question,
            "attempt": self.attempt,
            "result": is_correct(self.question, self.attempt, self.question_type, self.question_id, self.independent_var),
        }


def check_solution(question_type, question_id, attempt):

    if is_question(question_type, question_id):
        question = attempt.get("question")
        attempt = attempt.get("attempt")
        attempt_response = Attempt(question, attempt, question_type, question_id)
        status = 200

    else:
        attempt_response = AttemptError()
        status = 404

    return attempt_response, status
