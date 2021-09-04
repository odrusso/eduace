from sympy import symbols, latex, Eq

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
    def __init__(self, seed):
        self.description = ""
        self.question = ""
        self.seed = seed
    
    @property
    def json(self):
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
    question_dict = {}

    for question_type, question_type_items in QUESTION_MAPPING.items():
        question_dict[question_type] = list(question_type_items.keys())

    return question_dict, 200
