

class AttemptResponse:
    def __init__(self, question, attempt, result):
        self.question = question
        self.attempt = attempt
        self.result = result

    @property
    def json(self):
        return {
            "question": self.question,
            "attempt": self.attempt,
            "result": self.result
        }
