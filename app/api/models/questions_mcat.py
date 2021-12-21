from sympy import symbols, latex, Eq

from app.api.models.question import Question
from app.api.services import maths_service


class MCATQuestion1(Question):
    def __init__(self, seed, independent_var="x"):
        super().__init__(seed, independent_var)

        var = symbols(self.independent_var)
        var_a, var_b = maths_service.integer_coefficients(amount=2, seed=self.seed)

        self.description = "Solve a linear equation."
        self.question = latex(Eq(var_a * var + var_b, 0))
        self.independent_var = independent_var
