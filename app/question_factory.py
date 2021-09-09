# pylint: disable=C0103
from sympy import Eq, latex, symbols

from . import maths_service


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
