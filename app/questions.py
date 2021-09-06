from sympy import symbols, latex, Eq
from . import maths_service


class QuestionError(Exception):
    def __init__(self):
        self.description = "Question not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class QuestionTypeError(Exception):
    def __init__(self):
        self.description = "Question type not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class Question:
    def __init__(self, seed, independent_var):
        self.description = ""
        self.question = ""
        self.seed = seed
        self.independent_var = independent_var
    
    @property
    def json(self):
        return {
            "description": self.description,
            "question": self.question,
            "independent_var": self.independent_var,
        }


class MCATQuestion1(Question):
    def __init__(self, seed, independent_var="x"):
        super().__init__(seed, independent_var)

        var = symbols(self.independent_var)
        a, b = maths_service.integer_coefficients(amount=2, seed=self.seed)

        self.description = "Solve a linear equation."
        self.question = latex(Eq(a * var + b, 0))
        self.independent_var = independent_var


QUESTION_MAPPING = {
    'mcat': {
        '1': MCATQuestion1,
    },
}


def get_question(question_type, question_id, seed):
    if question_type := QUESTION_MAPPING.get(question_type, None):
        if question := question_type.get(question_id, None):
            question = question(seed)
            status = 200
        else:
            question = QuestionError()
            status = 404
    else:
        question = QuestionTypeError()
        status = 404

    return question, status


def get_all_questions():
    question_response = {"questions": []}

    for question_type, question_type_items in QUESTION_MAPPING.items():
        question_response["questions"].append({
            "questionTypeName": question_type,
            "questionIds": list(question_type_items.keys())
        })

    return question_response, 200
