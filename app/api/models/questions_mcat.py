from sympy import symbols, latex, Eq, Integer, Pow, simplify
from sympy.parsing.latex import parse_latex

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
        expected_solution = - Integer(self.var_b) / Integer(self.var_a)
        return parsed_attempt.rhs.equals(expected_solution)


class MCATQuestion2(Question):
    def __init__(self, seed, independent_var="x"):
        super().__init__(seed, independent_var)

        self.description = "Adding like terms."

        self.letter_var = symbols("a")
        self.co1, self.co2, self.co3, self.co4 = maths_service.integer_coefficients(amount=4, seed=self.seed)

        question_first_part_latex = latex(self.letter_var * self.co1 + self.co2)

        question_second_part_sign = "+" if self.co3 > 0 else ""
        question_second_part_latex = f"{question_second_part_sign} {latex(self.letter_var * self.co3)}"

        question_third_part_sign = "+" if self.co4 > 0 else ""
        question_third_part_latex = f"{question_third_part_sign} {self.co4}"

        self.question = f"{question_first_part_latex} {question_second_part_latex} {question_third_part_latex}"

    def validate_attempt(self, attempt_latex_string):
        parsed_attempt = parse_latex(attempt_latex_string)
        expected_solution = ((self.co1 + self.co3) * self.letter_var) + (self.co2 + self.co4)
        return parsed_attempt.equals(expected_solution)


class MCATQuestion3(Question):
    def __init__(self, seed, independent_var="x"):
        super().__init__(seed, independent_var)
        self.description = "Powers of powers."

        letter_a = symbols("a")
        letter_b = symbols("b")

        co1, = maths_service.positive_integer_coefficients(amount=1, number_range=(1, 5), seed=self.seed)
        power1, power2 = maths_service.positive_integer_coefficients(amount=2,
                                                                     number_range=(1, 3),
                                                                     seed=self.seed)
        power3, = maths_service.positive_integer_coefficients(amount=1,
                                                              number_range=(2, 3),
                                                              seed=self.seed)

        self.question_raw = Pow(co1 * (letter_a ** power1) * (letter_b ** power2), power3, evaluate=False)

        self.question = latex(self.question_raw)

    def validate_attempt(self, attempt_latex_string):
        parsed_attempt = parse_latex(attempt_latex_string)
        expected_solution = simplify(self.question_raw)
        return parsed_attempt.equals(expected_solution)
