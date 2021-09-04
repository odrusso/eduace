from sympy import symbols, latex, Eq

class QuestionError:
    def __init__(self):
        self.description = "Question not found."


class QuestionTypeError:
    def __init__(self):
        self.description = "Question type not found."


class Question:
    def __init__(self, seed):
        self.description = ""
        self.question = ""
        self.seed = seed
    
    @property
    def __dict__(self):
        return {
            "description": self.description,
            "question": self.question,
        }


class MCATQuestion1(Question):
    def __init__(self, seed):
        super().__init__(seed)

        x = symbols("x")
        ## TODO: Use seed
        a = 2
        b = 3
        self.description = "Solve a linear equation."
        self.question = latex(Eq(a * x + b, 0))


QUESTION_MAPPING = {
    'mcat': {
        '1': MCATQuestion1,
    },
}


def get_question(question_type, question_id, seed):

    if QUESTION_MAPPING.get(question_type, None):
        if QUESTION_MAPPING.get(question_type).get(question_id, None):
            question = QUESTION_MAPPING.get(question_type).get(question_id)(seed)
        else:
            question = QuestionError()
    else:
        question = QuestionTypeError()

    return question