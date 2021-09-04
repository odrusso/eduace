from sympy import symbols, latex, Eq, Rational


class SolutionError(Exception):
    def __init__(self):
        self.description = "Solution or question not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class SolutionTypeError(Exception):
    def __init__(self):
        self.description = "Solution or question type not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


class Solution:
    def __init__(self, seed):
        self.description = ""
        self.solution = []
        self.seed = seed
    
    @property
    def json(self):
        return {
            "description": self.description,
            "solution": self.solution
        }


class MCATSolution1(Solution):
    def __init__(self, seed):
        super().__init__(seed)
        # TODO: write services class to handle coefficient generation in reproduceable way
        x = symbols('x')
        a = 2
        b = 3

        self.description = "Too easy"
        self.solution = [latex(Eq(x, -1 * Rational(b, a)))]


SOLUTION_MAPPING = {
    'mcat': {
        '1': MCATSolution1,
    },
}


def get_solution(question_type, question_id, seed):

    if question_type := SOLUTION_MAPPING.get(question_type, None):
        if question := question_type.get(question_id, None):
            solution = question(seed)
            status = 200
        else:
            solution = SolutionError()
            status = 404
    else:
        solution = SolutionTypeError()
        status = 404

    return solution, status
