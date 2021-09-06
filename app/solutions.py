from .solution_service import is_correct
from .questions import QUESTION_MAPPING


class AttemptError(Exception):
    def __init__(self):
        self.description = "Solution or question not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class AttemptTypeError(Exception):
    def __init__(self):
        self.description = "Solution or question type not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class Attempt:
    def __init__(self, question, attempt):
        self.question = question
        self.attempt = attempt
    
    @property
    def json(self):
        return {
            "question": self.question,
            "attempt": self.attempt,
            "result": is_correct(self.question, self.attempt),
        }


def check_solution(question_type, question_id, attempt):

    question = attempt.get("question")
    attempt = attempt.get("attempt")

    if question_type := QUESTION_MAPPING.get(question_type, None):
        if question_type.get(question_id, None):
            attempt_response = Attempt(question, attempt)
            status = 200
        else:
            attempt_response = AttemptError()
            status = 404
    else:
        attempt_response = AttemptTypeError()
        status = 404

    return attempt_response, status
