# utf-8
# Python 3.6, SymPy 1.1.1
# http://github.com/odrusso/eduace

from sympy import *
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application, convert_xor, parse_expr
from random import randint, shuffle
from math import sqrt
# from lat2sym.process_latex import process_sympy


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
        """Initalised the basic vairables required for the class"""
        self.question_aspects = []
        self.answer_aspects = []
        self.question_raw = 0
        self.answer_raw = 0

    def generate_question(self, question_type, route=None):
        """Takes the question number inputed and executes the generation function"""
        if route is None:
            eval("self.generate_question_mcat_" + question_type.replace(".", "_") + "()")
        else:
            eval("self.generate_question_mcat_" + question_type.replace(".", "_") + "(" + str(route) + ")")

    def random_co(self, minimum, maximum, number, zero=False, one=True):
        """Generates random numbers between 2 bounds, with extra features"""
        co_range = list(range(minimum, maximum+1))
        shuffle(co_range)

        if not one and not zero:
            if 1 in co_range:
                co_range.remove(1)
            if -1 in co_range:
                co_range.remove(-1)
            if 0 in co_range:
                co_range.remove(0)

        elif not one:
            if 1 in co_range:
                co_range.remove(1)
            if -1 in co_range:
                co_range.remove(-1)

        elif not zero:
            if 0 in co_range:
                co_range.remove(0)

        while len(co_range) < number:
            co_range += co_range
            shuffle(co_range)

        return co_range[:number]

    def ppm(self, tester):
        """Takes a sympy value and returns a latex string sutiable for usage in a summation style question"""

        valid_sympy_types = [type(symbols('x') * 2), type(symbols('x')**2)]
        valid_sympy_numbers = [type(0), type(sympify(0)), type(sympify(10)), type(sympify(-1))]

        if tester == 0:
            return sympify(None)

        elif type(tester) == type(0):
            if tester > 0:
                return " + " + latex(tester)
            else:
                return latex(tester)

        elif type(tester) == type(symbols("x")):
            if len(tester.args) > 0:
                if type(tester.args[0]) in valid_sympy_numbers:
                    if tester.args[0] > 0:
                        return " + " + latex(tester)
                    else:
                        return latex(tester)
                else:
                    return " + " + latex(tester)
            else:
                return " + " + latex(tester)

        elif type(tester) in valid_sympy_types:
            if type(tester.args[0]) in valid_sympy_numbers:
                if tester.args[0] > 0:
                    return " + " + latex(tester)
                else:
                    return latex(tester)
            else:
                return " + " + latex(tester)

        else:
            return " + " + latex(tester)

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

    def generate_question_mcat_1_1_1(self, route=None):
        """Question MACT 1.1.1"""

        if route is None:
            route = self.random_co(1, 3, 1)[0]

        self.route = route

        # TESTING
        route = 1

        if route == 1:
            x, y = symbols("x y")

            xa, xb = self.random_co(-5, 5, 2, zero=False, one=False)
            ca, cb = self.random_co(-10, 10, 2)

            self.question_raw = Add(xa*x, ca, xb*x, cb, evaluate=False)
            question_order = '&' + str(xa) + 'x ' + "%+d" % (ca) + " %+dx" % (xb) + " %+d" % (cb)
            self.question_aspects = [r'&\text{Simplify: }', question_order]

            self.answer_raw = self.question_raw.simplify()

        elif route == 2:
            a = symbols("a")

            xa, xb, xc, xd = self.random_co(-8, 8, 4, zero=False, one=False)

            self.question_raw = Add(xa*a**2 + xb*a, + xc*a**2 + xd*a, evaluate=False)

            self.question_aspects = [r'&\text{Simplify: }', '&' + latex(self.question_raw)]

            self.answer_raw = self.question_raw.simplify().expand()

        elif route == 3:
            a, b = symbols("a b")

            xa, xb, xc, xd, xe, xf = self.random_co(-8, 8, 6, zero=True, one=True)

            ca, cb = self.random_co(-10, 10, 2, zero=False)

            question_elements = [xa*a, xb*b, xc*a*b, xd*a, xe*b, xf*a*b, ca, cb]
            shuffle(question_elements)
            deletions = self.random_co(0, 2, 1, True, True)
            question_elements = question_elements[deletions[0]:]

            for element in question_elements:
                self.question_raw = Add(self.question_raw, element, evaluate=False)

            if question_elements[0] != 0:
                question_latex = "&" + latex(question_elements.pop(0))
            else:
                while question_elements[0] == 0:
                    shuffle(question_elements)
                else:
                    question_latex = "&" + latex(question_elements.pop(0))

            for item in question_elements:
                insertable = self.ppm(item)
                if insertable != None:
                    question_latex += insertable

            self.question_aspects = [r'&\text{Simplify: }', question_latex]

            self.answer_raw = latex(self.question_raw.simplify().expand())

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_1_2(self, route=None):
        """Question MACT 1.1.2"""

        if route is None:
            route = self.random_co(1, 1, 1)[0]

        self.route = route

        # TESTING
        route = 2

        if route == 1:
            a, b = symbols("a b")
            xa, xb = self.random_co(-2, 4, 2, zero=False, one=False)
            self.question_raw = Mul(xa*a**2, xb*a, evaluate=False)
            self.question_aspects = [r'&\text{Simplify: }', "&" + latex(xa*a**2) + r'\times ' + latex(xb*a)]
            self.answer_raw = self.question_raw.simplify()

        elif route == 2:
            t, s = symbols("t s")
            xa, xb = self.random_co(-3, 4, 2)
            pa, pb, pc, pd = self.random_co(0, 8, 4, one=True)
            self.question_raw = Mul(xa*t**pa*s**pb, xb*t**pc*s**pd, evaluate=False)
            self.question_aspects = [r'&\text{Simplify: }', "&" + latex(xa) + "s^{" + latex(pa) + '} t^{' + latex(pb) + r"} \times " + latex(xb) + "s^{" + latex(pc) + "}t^{" + latex(pd) + '}']
            self.answer_raw = self.question_raw.simplify()

        self.answer_aspects = [latex(self.answer_raw)]



def testing():
    """Testing for program structure and question types"""

    new_question = MathsQuestion()
    new_question.generate_question(input("Enter question number: "))
    init_printing()

    print()

    print("Question Raw: ")
    print(new_question.question_raw)

    print()

    print("Question Aspects: ")

    for line in new_question.question_aspects:
        print(line)

    print()

    print("Answer Raw: ")
    print(latex(new_question.answer_raw))

    print()

    print("Answer Aspects: ")

    for line in new_question.answer_aspects:
        print(line)

def ppm_testing():

    x, y = symbols("x y")

    foo = MathsQuestion()

    print(foo.ppm(6))

    print(foo.ppm(x))

    print(foo.ppm(x * y))

    print(foo.ppm(2))

    print(foo.ppm(2 * x))

    print(foo.ppm(2 * x * y))

    print(foo.ppm(y * y))


    print(foo.ppm(-x))

    print(foo.ppm(-x * y))

    print(foo.ppm(-2))

    print(foo.ppm(-1))

    print("printing 0")
    print(foo.ppm(0))

    print(foo.ppm(-2 * x))

    print(foo.ppm(-2 * x * y))

    print(foo.ppm(-y * y))


def testing111():

    while True:
        new_question = MathsQuestion()
        new_question.generate_question("1.1.1")
        print(new_question.route)
        print(new_question.question_raw)
        print(new_question.question_aspects)
        print(new_question.answer_raw)
        print(new_question.answer_aspects)

        input()


if __name__ == "__main__":
    testing()
