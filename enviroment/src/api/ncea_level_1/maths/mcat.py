from sympy import *
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application, convert_xor, parse_expr
from math import sqrt

from lat2sym.process_latex import process_sympy

import random

from random import randint

class Data():
    def __init__(self):
        self.context_options = ["rectangle", "paddock", "pond", "playground", "pool", "park"]

    def choose(self, full_list):
        num = randint(0, len(full_list) - 1)
        return full_list[num]
    
data = Data()


class CATPaper():
    """Class for storing entire data-strucute of a Level 1 C.A.T exam paper"""
    """
           - Define paper strucutre
           - Randomise question order?
          - Call question generation for each determined question
    """

    def __init__(self):
        self.questions = []
        self.generate_paper()

    def generate_paper(self):
        None


class MathsQuestion():
    """Class for storing data-structure of an indiviual question
            - Need a comprehensive list of types of questions possible in CAT.
            - Function appends items to question_aspects and answer_aspects (string, equation, diagram, table, etc)
    """

    def __init__(self):
        self.question_aspects = []
        self.answer_aspects = []
        self.question_raw = None
        self.answer_raw = None

    def generate_question(self, question_type):
        eval("self.generate_question_mcat_" + question_type + "()")

    def return_latex(self, valueable):
        return latex(valueable)

    def random_co(self, minimum, maximum, number, zero=False):
        co_range = list(range(minimum, maximum))
        random.shuffle(co_range)
        if zero:
            return co_range[:number]
        else:
            if 0 in co_range:
                co_range.remove(0)
            return co_range[:number]

    def generate_question_factor_1(self):
        x, y = symbols("x y")
        xa, xb = self.random_co(-8, 8, 2)
        self.answer_raw = (x+xa)*(x+xb)
        self.question_raw = expand(self.answer_raw)
        line1 = ["A", data.choose(data.context_options), "has an area of", str(self.question_raw)]
        line2 = ["What are the lengths of the sides in terms of x?"]
        self.question_aspects = [line1, line2]

    def generate_question_factor_2(self):
        x, y = symbols("x y")
        xa, xb = self.random_co(-8, 8, 2)
        self.answer_raw = (x+xa)*(x+xb)
        self.question_raw = expand(self.answer_raw)
        self.answer_raw = (x+xb)
        line1 = ["A", data.choose(data.context_options), "has an area of", str(self.question_raw)]
        line2 = ["One side can be described as", str((x+xa))]
        line3 = ["What are the lengths of the sides in terms of x?"]
        self.question_aspects = [line1, line2, line3]

    def generate_question_quadratic_solve(self):
        x, y = symbols("x y")
        xa, xb = self.random_co(-8, 8, 2)
        xc = self.random_co(2, 4, 1)[0]
        answer_backwards = (xc*x+xa)*(x+xb)
        self.question_raw = expand(answer_backwards)
        self.answer_raw = solve(self.question_raw)
        self.question_aspects = [["Solve", self.question_raw]]
        self.answer_aspects = [answer_backwards, self.answer_raw]

    def generate_question_quote_sim(self):
        x = symbols("x")
        xa, xb, xc, xd = self.random_co(-5, 5, 4)
        self.answer_raw = (x + xa) / (xb*x)
        self.question_raw = expand((x + xa)*(x + xc)) / expand((x + xc)*(xb*x))
        self.question_aspects = [["Simplify", self.question_raw]]
        self.answer_aspects = [["Factorise", str((x + xa)*(x + xc)/(x + xc)*(xb*x))], [self.answer_raw]]

    def generate_question_quote_solve(self):
        """WARNING: HIGHLY UNOPTIMISED"""
        x = symbols("x")

        xa, xb = self.random_co(-10, 10, 2)
        xc, xd = self.random_co(0, 6, 2)

        while sqrt(xc*xd).is_integer():
            xc, xd = self.random_co(0, 6, 2)

        xb, xc, xd, xe = self.random_co(-7, 7, 4)
        self.question_raw = Eq(expand((x + xa) * (x + xb)) / ((x + xa) * (x + xc)), (x / xd))
        self.answer_raw = solve(self.question_raw)
        self.answer_aspects = [["x =", str(self.answer_raw)]]
        self.question_aspects = [["Solve", self.question_raw]]

    def evaluate_answer(self, user_input):
        """evaluates the equivlence of a plaintext answer input"""
        tfms = (standard_transformations + (implicit_multiplication_application,))
        user_input.replace(" ", "")
        if user_input == str(self.answer_raw):
            return [True, "Correct"]
        else:
            try:
                user_parsed = parse_expr(user_input, transformations=tfms)

                # Testing
                # print("User answer: " +  str(user_parsed))
                # print("Real answer: " + str(self.answer_raw))

                if user_parsed == self.answer_raw:
                    return [True, "Correct"]
                elif user_parsed - self.answer_raw == 0:
                    return [True, "Correct", "Your answer *may* not be fully simplified"]
                elif simplify(simplify(user_parsed) - simplify(self.answer_raw)) == 0:
                    return [False, "Partially Correct", "Your answer was not fully simplified"]
                else:
                    return [False, "Incorrect"]
            except SyntaxError:
                return [False, "Invalid entry"]
            except:
                return [False, "An Error has occurred"]


def testing():
    """Testing for program structure and question types"""

    new_question = MathsQuestion()
    new_question.generate_question('factor_2')
    init_printing()
    print(latex(new_question.question_raw))
    print(latex(new_question.answer_raw))

if __name__ == "__main__":
    testing()