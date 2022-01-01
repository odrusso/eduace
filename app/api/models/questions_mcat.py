from sympy import symbols, latex, Eq
from sympy.parsing.latex import LaTeXParsingError, parse_latex

from app.api.models.question import Question
from app.api.services import maths_service


class MCATQuestion1(Question):
    def __init__(self, seed, independent_var="x"):
        super().__init__(seed, independent_var)

        var = symbols(self.independent_var)
        self.var_a, self.var_b = maths_service.integer_coefficients(amount=2, seed=self.seed)

        self.description = "Solve a linear equation."
        self.question = latex(Eq(self.var_a * var + self.var_b, 0))
        self.independent_var = independent_var

    def validate_attempt(self, attempt_latex_string):
        parsed_attempt = parse_latex(attempt_latex_string)
        return parsed_attempt.rhs == - self.var_b / self.var_a