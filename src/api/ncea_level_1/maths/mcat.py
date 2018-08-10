# utf-8
# Python 3.6, SymPy 1.1.1
# http://github.com/odrusso/eduace

from sympy import *
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application, convert_xor, parse_expr
from random import randint, shuffle
from math import sqrt
#from lat2sym.process_latex import process_sympy


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

    def __init__(self, question_number="0.0.0"):
        """Initialise the basic variables required for the class"""
        self.question_aspects = []
        self.answer_aspects = []
        self.question_raw = 0
        self.answer_raw = 0
        self.question_description = None
        self.route = None

        if question_number != "0.0.0":
            self.generate_question(question_number)

    def generate_question(self, question_type):
        """Takes the question number inputed and executes the generation function"""
        if self.route is None:
            eval("self.generate_question_mcat_" + question_type.replace(".", "_") + "()")
        else:
            eval("self.generate_question_mcat_" + question_type.replace(".", "_") + "(" + str(self.route) + ")")

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
        user_input = process_sympy(user_input)

        if user_input == str(self.answer_raw):
            return [True, "Correct"]
        else:
            try:
                # Testing
                # print("User answer: " +  str(user_parsed))
                # print("Real answer: " + str(self.answer_raw))

                if user_input == self.answer_raw:
                    return [True, "Correct"]
                elif user_input - self.answer_raw == 0:
                    return [True, "Correct", "Your answer *may* not be fully simplified"]
                elif simplify(simplify(user_input) - simplify(self.answer_raw)) == 0:
                    return [False, "Partially Correct", "Your answer was not fully simplified"]
                else:
                    return [False, "Incorrect"]
            except SyntaxError:
                return [False, "Invalid entry"]
            # except Exception as e:
            #     print(e)

    def generate_question_mcat_1_1_1(self):
        """Question MACT 1.1.1"""

        self.question_description = "Collect like terms."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x, y = symbols("x y")

            xa, xb = self.random_co(-5, 5, 2, zero=False, one=False)
            ca, cb = self.random_co(-10, 10, 2)

            self.question_raw = Add(xa*x, ca, xb*x, cb, evaluate=False)
            question_order = '&' + str(xa) + 'x ' + "%+d" % (ca) + " %+dx" % (xb) + " %+d" % (cb)
            self.question_aspects = [r'&\text{Simplify: }', question_order]

            self.answer_raw = self.question_raw.simplify()

        elif self.route == 2:
            a = symbols("a")

            xa, xb, xc, xd = self.random_co(-8, 8, 4, zero=False, one=False)

            self.question_raw = Add(xa*a**2 + xb*a, + xc*a**2 + xd*a, evaluate=False)

            self.question_aspects = [r'&\text{Simplify: }', '&' + latex(self.question_raw)]

            self.answer_raw = self.question_raw.simplify().expand()

        elif self.route == 3:
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
                if insertable is not None:
                    question_latex += insertable

            self.question_aspects = [r'&\text{Simplify: }', question_latex]

            self.answer_raw = latex(self.question_raw.simplify().expand())

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_1_2(self):
        """Question MCAT 1.1.2"""

        self.question_description = "Multiplying out terms."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            a, b = symbols("a b")
            xa, xb = self.random_co(-2, 4, 2, zero=False, one=False)
            self.question_raw = Mul(xa*a**2, xb*a, evaluate=False)
            self.question_aspects = [r'&\text{Simplify: }', "&" + latex(xa*a**2) + r'\times ' + latex(xb*a)]
            self.answer_raw = self.question_raw.simplify()

        elif self.route == 2:
            t, s = symbols("t s")
            xa, xb = self.random_co(-3, 4, 2)
            pa, pb, pc, pd = self.random_co(0, 8, 4, one=True)
            self.question_raw = Mul(xa*t**pa*s**pb, xb*t**pc*s**pd, evaluate=False)
            self.question_aspects = [r'&\text{Simplify: }', "&" + latex(xa) + "s^{" + latex(pa) + '} t^{' + latex(pb) + r"} \times " + latex(xb) + "s^{" + latex(pc) + "}t^{" + latex(pd) + '}']
            self.answer_raw = self.question_raw.simplify()

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_1_3(self):
        """Question MCAT 1.1.3"""

        self.question_description = "Powers of powers."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols('x')

            a, b = self.random_co(2, 5, 2)
            c = self.random_co(2, 3, 1)[0]

            self.question_raw = Pow(c * x ** a, b, evaluate=False)
            self.answer_raw = self.question_raw.simplify()

            self.question_aspects = [r'\text{Simplify: }', latex(self.question_raw)]
            self.answer_aspects = [r' \times '.join([latex(c * x ** a)]*b), latex(self.answer_raw)]

        elif self.route == 2:
            x, y = symbols('x y')

            a, b, c = self.random_co(2, 5, 3)
            d = self.random_co(2, 3, 1)[0]

            self.question_raw = Pow(a * x ** b * y ** c, d, evaluate=False)
            self.answer_raw = self.question_raw.simplify()

            self.question_aspects = [r'\text{Simplify: }', latex(self.question_raw)]
            self.answer_aspects = [r' \times '.join([latex(a * x ** b * y **c)] * b), latex(self.answer_raw)]

    def generate_question_mcat_1_1_4(self):
        """Question MCAT 1.1.4"""

        self.question_description = "Square roots of powers."

        x, y = symbols('x y')

        a, b, c = self.random_co(2, 5, 3)

        self.question_raw = Pow((a**2)*x**(b*2)*y**(c*2), 0.5, evaluate=False)
        self.question_aspects = [r'\text{Simplify: }', r'\sqrt{' + latex((a**2)*x**(b*2)*y**(c*2)) + "}"]

        self.answer_raw = a*x**b*y**c
        self.answer_aspects = [r"\sqrt{" + latex(a**2) + r"} \times x ^ \frac{" + latex(b*2) + r'}{2} \times y ^ \frac{'
                                + latex(c*2) + r"}{2}" , latex(self.answer_raw)]

    def generate_question_mcat_1_2_1(self):
        """Question MCAT 1.2.1"""

        self.question_description = "Expanding out one bracket."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols('x')

            a = self.random_co(2, 6, 1)[0]
            b, c = self.random_co(-5, 5, 2, one=False)

            self.question_raw = Mul(a*x, b*x + c, evaluate=False)
            self.question_aspects = [r"\text{Expand: ", latex(self.question_raw)]

            self.answer_raw = a*x*b*x + a*x*c
            self.answer_aspects = [latex(self.answer_raw)]

        elif self.route == 2:
            a, b = symbols('a b')

            a1 = self.random_co(2, 6, 1)[0]
            b1, c1, d1 = self.random_co(-5, 5, 3, one=False)

            self.question_raw = Mul(a*a1, a*b1 + b*c1 + d1, evaluate=False)
            self.question_aspects = [r"\text{Expand: ", latex(self.question_raw)]

            self.answer_raw = a*a1*a*b1 + a*a1*b*c1 + a*a1*d1
            self.answer_aspects = [latex(self.answer_raw)]

        elif self.route == 3:
            x = symbols('x')

            a, b, c, d, e = self.random_co(-5, 5, 5)
            pom = self.random_co(-1, 1, 1)[0]

            self.question_raw = Add(Mul(a, b*x+c, evaluate=False), pom*(d*x + e), evaluate=False)

            self.question_aspects = [r"\text{Expand: }", latex(Mul(a, b*x+c, evaluate=False)) + self.ppm(pom)[0] + r'\left(' + latex(pom*(d*x + e)) + r"\right)"]

    def generate_question_mcat_1_2_2(self):
        """Question MCAT 1.2.2"""

        self.question_description = "Expanding out two brackets."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols('x')
            a, b = self.random_co(-5, 5, 2, one=False)

            self.question_raw = Mul(x + a, x + b, evaluate=False)
            self.question_aspects = [r'\text{Expand: }', latex(self.question_raw)]

            self.answer_raw = self.question_raw.expand()
            self.answer_aspects = [latex(self.answer_raw)]

        elif self.route == 2:
            x = symbols('x')
            a, b = self.random_co(-5, 5, 2, one=False)
            c = self.random_co(2, 4, 1)[0]

            self.question_raw = Mul(c*x + a, x + b, evaluate=False)
            self.question_aspects = [r'\text{Expand: }', latex(self.question_raw)]

            self.answer_raw = self.question_raw.expand()
            self.answer_aspects = [latex(self.answer_raw)]

        elif self.route == 3:
            x, y = symbols('x y')

            a, b = self.random_co(2, 5, 2, one=False)
            c, d = self.random_co(-1, 1, 2)

            self.question_raw = Mul(a*x + c*y, b*x + d*y, evaluate=False)
            self.question_aspects = [r"\text{Simplify: }", latex(self.question_raw)]

            self.answer_raw = a*b*x*x + a*x*d*y + c*y*b*x + c*y*d*y
            self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_3_1(self):
        """Question MCAT 1.3.1"""

        self.question_description = "Finding common factors."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols('x')
            a = self.random_co(3, 6, 1)[0]
            b = self.random_co(-5, 5, 1, one=False)[0]

            self.question_raw = a * x ** 2 + a * b * x
            self.question_aspects = [r'\text{Expand: }', latex(self.question_raw)]

            self.answer_raw = Mul(a, x + b, evaluate=False)
            self.answer_aspects = [latex(self.answer_raw)]

        elif self.route == 2:
            a, b = symbols('a b')
            c, d, e = self.random_co(2, 8, 3)

            self.answer_raw = Mul(c*a*b, d*a + e, evaluate=False)

    def generate_question_mcat_1_3_2(self):
        """Question MCAT 1.3.2"""

        self.question_description = "Factorising quadratics in the form x^2 + bx + c"

        x = symbols("x")
        a, b = self.random_co(-4, 4, 2)
        self.question_raw = expand((x + a) * (x + b))
        self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
        self.answer_raw = (x + a) * (x + b)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_3_3(self):
        """Question MCAT 1.3.3 negative numbers potentially an issue?"""

        self.question_description = "Factorising quadratics in the form ax^2 + bx + c"

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            a, b, mult = self.random_co(-7, 7, 3, zero=False)
            self.question_raw = expand(mult * (x + a) * (x + b))
            self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
            self.answer_raw = Mul(mult, (x + a), (x + b))

        elif self.route == 2:
            x = symbols("x")
            a, b = (2, 4)
            while gcd(a, b) != 1:
                a, b, c = self.random_co(-7, 7, 3, zero=False, one=False)
            self.question_raw = expand((a * x + b) * (x + c))
            self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
            self.answer_raw = Mul((a * x + b), (x + c))

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_1_3_4(self):
        """Question MCAT 1.3.4"""

        self.question_description = "Factorising difference of two squares."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            a, b = symbols("a b")
            xb = self.random_co(2, 10, 1)[0]
            self.question_raw = a ** 2 - (xb) ** 2
            self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
            self.answer_raw = (a - xb) * (a + xb)

        elif self.route == 2:
            a, b = symbols("a b")
            xa = self.random_co(2,10,1)[0]
            self.question_raw = (xa * a) ** 2 - 1
            self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
            self.answer_raw = (xa - 1) * (xa + 1)

        elif self.route == 3:
            a, b = symbols("a b")
            xa, xb = self.random_co(2,10,2)
            self.question_raw = (xa * a) ** 2 - xb ** 2
            self.question_aspects = [r'&\text{Factorise: }', '&' + latex(self.question_raw)]
            self.answer_raw = (xa * a - xb) * (xa * a + xb)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_2_1_1(self):
        """Question MCAT 2.1.1"""

        self.question_description = "Substituting into a formula"

        equations = [
                        ['Eq(v, u + a*t)', symbols('v, u, a, t')],
                        ['Eq(d, u*t + Rational(1, 2) * a * t ** 2)', symbols('d, u, t, a')],
                        ['Eq(d, Rational(1, 2)*(u + v) * t)', symbols('d, u, v, t')],
                        ['Eq(A, pi * r ** 2)', symbols('A, r')],
                        ['Eq(A, 4 * pi * r ** 2)', symbols('A, r')],
                        ['Eq(V, S(4) / 3 * pi * r ** 3)', symbols('V, r')],
                        ['Eq(F, S(9) / 5 * C + 32)', symbols('F, C')],
                        ['Eq(C, S(5) / 9 * (F - 32))', symbols('C, F')],
                        ['Eq(A, 2*pi*r*(h+r))', symbols('A, r, h')],
                        ['Eq(R, (2*f*(n-1)) / (q + 1))', symbols('R, f, n, q')],
                        ['Eq(p, (a - b) / (a + b))', symbols('p, a, b')],
                        ['Eq(E, Rational(1, 2) * m * v ** 2)', symbols('E, m, v')],
                        ['Eq(E, Rational(1, 2) * k * x ** 2)', symbols('E, k, x')],
                        ['Eq(F, (m * v ** 2) / r)', symbols('F, m, v, r')],
                        ['Eq(T, 2*pi*sqrt(l / g))', symbols('T, l, g')],
                        ['Eq(T, 2*pi*sqrt(m / k))', symbols('T, m, k')]
                     ]

        shuffle(equations)
        equation, variables = equations[0]

        self.question_raw = sympify(equation)
        eqn = sympify(equation)

        values = {}

        for variable in variables[1:]:
            values[variable] = self.random_co(1, 10, 1)[0]

        subs_string = ""
        for value in values.keys():
            subs_string += latex(value)
            subs_string += " = "
            subs_string += latex(values[value])
            subs_string += ", "

        self.question_aspects = [[r"\text{ Substitute values }" + subs_string + r"\text{ into: }", latex(self.question_raw)]]

        for value in values.keys():
            eqn = eqn.subs(value, values[value])

        self.answer_raw = solve(eqn)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_2_1_2(self):
        """Question MCAT 2.1.2"""

        self.question_description = "Rearranging formulas."

        equations = [
            ['Eq(v, u + a*t)', symbols('v, u, a, t')],
            # ['Eq(d, u*t + Rational(1, 2) * a * t ** 2)', symbols('d, u, t, a')],
            ['Eq(d, Rational(1, 2)*(u + v) * t)', symbols('d, u, v, t')],
            ['Eq(A, pi * r ** 2)', symbols('A, r')],
            ['Eq(A, 4 * pi * r ** 2)', symbols('A, r')],
            ['Eq(V, (S(4) / 3) * pi * r ** 3)', symbols('V, r')],
            ['Eq(F, S(9) / 5 * C + 32)', symbols('F, C')],
            ['Eq(C, Mul(S(5) / 9, (F - 32), evaluate=False))', symbols('C, F')],
            # ['Eq(A, 2*pi*r*(h+r))', symbols('A, r, h')],
            # ['Eq(R, (2*f*(n-1)) / (q + 1))', symbols('R, f, n, q')],
            # ['Eq(p, (a - b) / (a + b))', symbols('p, a, b')],
            ['Eq(e, Rational(1, 2) * m * v ** 2)', symbols('e, m, v')],
            ['Eq(e, Rational(1, 2) * k * x ** 2)', symbols('e, k, x')],
            ['Eq(F, (m * v ** 2) / r)', symbols('F, m, v, r')],
            ['Eq(T, 2*pi*sqrt(l / g))', symbols('T, l, g')],
            ['Eq(T, 2*pi*sqrt(m / k))', symbols('T, m, k')]
        ]

        shuffle(equations)

        equation, variables = equations[0]

        self.question_raw = sympify(equation)

        candidate_vars = list(variables)[1:]

        shuffle(candidate_vars)

        variable = candidate_vars[0]

        self.question_aspects = [r'\text{Rearrange }' + latex(self.question_raw) + r'\text{ for }' + latex(variable)]

        if len(solve(self.question_raw, variable)) == 1:
            self.answer_raw = solve(self.question_raw, variable)[0]

        elif len(solve(self.question_raw, variable)) == 2:
            self.answer_raw = solve(self.question_raw, variable)[1]

        else:
            self.answer_raw = solve(self.question_raw, variable)[0]

        self.answer_aspects = [Eq(variable, self.answer_raw)]

    def generate_question_mcat_2_3_2(self):
        """Question MCAT 2.3.2"""

        self.question_description = "Simplifying by factoring and cancelling."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols('x')
            a, b = self.random_co(-8, 8, 2)
            self.question_raw = expand((x + a) * (x + b)) / (x + b)
            self.question_aspects = [r'Simplify: ' + latex(self.question_raw)]
            self.answer_raw = simplify(self.question_raw)

        elif self.route == 2:
            x = symbols('x')
            a, b, c = self.random_co(-8, 8, 3, zero=False, one=False)
            self.question_raw = expand((x + a) * (x + b)) / expand((c * x * (x + a)))
            self.question_aspects = [r'Simplify: ' + latex(self.question_raw)]
            self.answer_raw = simplify(self.question_raw)

        elif self.route == 3:
            x, y = symbols('x y')
            a, b, c, d = self.random_co(-8, 8, 4, zero=False, one=False)
            self.question_raw = (a * x * b * x) / expand(a * x * (c * x + d * y))
            self.question_aspects = [r'Simplify: ' + latex(self.question_raw)]
            self.answer_raw = simplify(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_3_1_1(self):
        """Question MCAT 3.1.1"""

        self.question_description = "Solving simple linear equations."

        if self.route is None:
            self.route = self.random_co(1, 5, 1)[0]

        if self.route == 1:
            x = symbols("x")
            adder, soln = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(x + adder, soln + adder)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = soln

        elif self.route == 2:
            x = symbols("x")
            multiple = self.random_co(3, 9, 1)[0]
            soln = self.random_co(-8, 8, 1, zero=False)[0]
            self.question_raw = Eq(multiple * x, multiple * soln)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = soln

        elif self.route == 3:
            x = symbols("x")
            a, b = self.random_co(3, 9, 2)
            self.question_raw = Eq(x / a, b)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = a * b

        elif self.route == 4:
            x = symbols("x")
            multiple, adder, soln = self.random_co(-10, 10, 3, zero=False)
            self.question_raw = Eq(multiple * x + adder, multiple * soln + adder)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = soln

        else:
            x = symbols("x")
            divisor, rhs = [1, 1]
            while divisor == rhs:
                divisor, rhs = self.random_co(3, 9, 2)
            adder = self.random_co(-9, 9, 1, zero=False)[0]
            soln = divisor * (rhs - adder)
            self.question_raw = Eq(x / divisor + adder, Rational(soln, divisor) + adder)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = soln

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_3_1_2(self):
        """Question MCAT 3.1.2 route 2 possibly too hard."""

        self.question_description = "Solving linear equations with like terms."


        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            multiple, adder, soln = self.random_co(-10, 10, 3, zero=False)
            self.question_raw = Eq(multiple * x + adder, multiple * soln + adder + (multiple * adder) * x)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        elif self.route == 2:
            x = symbols("x")
            a, b, c, d, e = self.random_co(-10, 10, 5, zero=False)
            self.question_raw = Eq(a * (b * x + c) + d * x, e)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = Rational((e - a * c), (a * b + d))

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_3_1_3(self):
        """Question MCAT 3.1.3 potentially too hard"""

        self.question_description = "Solving linear equations with fractions."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            a, b, c, d = self.random_co(1, 8, 4)
            self.question_raw = Eq(Add((x / a), (b * x) / c, evaluate=False), d)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        if self.route == 2:
            x = symbols("x")
            a, b, c, d = self.random_co(1, 8, 4)
            self.question_raw = Eq((b + x) / c, Add(d, -1 * (x / a), evaluate=False))
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_3_1_4(self):
        """MCAT question 3.1.4 possibly too easy"""

        self.question_description = "Solving linear equations without unique solutions."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            a, b, c = self.random_co(1, 15, 3)
            self.question_raw = Eq(factor(a * x + b), a * x - c, evaluate=False)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = [r'&\text{No solution.}']

        elif self.route == 2:
            x = symbols("x")
            a, b = self.random_co(1, 9, 2)
            self.question_raw = Eq(Add(factor(a * x + a * b), -1 * a * x, evaluate=False), b, evaluate=False)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = [r'&\text{Infinite solutions.}']

        self.answer_aspects = latex(self.answer_raw)

    def generate_question_mcat_4_1_1(self):
        """Question MCAT 4.1.1"""

        self.question_description = "Solving quadratic equations which are factorised and equal to zero."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            a, b = [2, 4]
            while gcd(a, b) != 1:
                a = self.random_co(1, 5, 1)[0]
                b, c = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(Mul((a * x + b), (x + c)), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        else:
            x = symbols("x")
            a, b = self.random_co(1, 8, 2)
            c = self.random_co(-8, 8, 1)[0]
            self.question_raw = Eq(Mul((a * x), (b * x + c)), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_4_1_2(self):
        """Question MCAT 4.1.2"""

        self.question_description = "Solving quadratic equations which are equal to zero, but not factorised."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        if self.route == 1:
            x = symbols("x")
            b, c = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(expand(Mul((x + b), (x + c))), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        elif self.route == 2:
            x = symbols("x")
            a, b = [2, 4]
            while gcd(a, b) != 1:
                a = self.random_co(1, 5, 1)[0]
                b, c = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(expand(Mul((a * x + b), (x + c))), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        elif self.route == 3:
            x = symbols("x")
            multiple = self.random_co(2, 5, 1)[0]
            b, c = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(expand(Mul((x + b), (x + c), multiple)), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        elif self.route == 4:
            x = symbols("x")
            multiple, a = self.random_co(2, 5, 2)
            self.question_raw = Eq(expand(Mul((x + a), (x - a), multiple)), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        else:
            x = symbols("x")
            a, b = self.random_co(1, 8, 2)
            c = self.random_co(-8, 8, 1)[0]
            self.question_raw = Eq(expand(Mul((a * x), (b * x + c))), 0)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_4_1_3(self):
        """Question MCAT 4.1.3"""

        self.question_description = "Solving quadratic equations which are not equal to zero."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols("x")
            b, c, adder = self.random_co(-8, 8, 3, zero=False)
            self.question_raw = Eq(expand((x + b) * (x + c)) + adder, adder)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        elif self.route == 2:
            x = symbols("x")
            b, c = self.random_co(-8, 8, 2)
            self.question_raw = Eq(expand((x + b) * (x + c)) - (b + c) * x - b * c, -1 * (b + c) * x - b * c)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        else:
            x = symbols("x")
            b, c = self.random_co(-8, 8, 2, zero=False)
            self.question_raw = Eq(x * (x + b + c), -1 * b * c)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_4_1_4(self):
        """Question MCAT 4.1.4"""

        self.question_description = "Solving quadratics in the form (x + a)^2 = b."

        if self.route is None:
            self.route = self.random_co(1, 2, 2)

        if self.route == 1:
            x = symbols("x")
            a, b = self.random_co(-9, 9, 2, zero=False)
            self.question_raw = Eq((x + a) ** 2, b ** 2)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        else:
            x = symbols("x")
            a = self.random_co(-9, 9, 1, zero=False)[0]
            b = self.random_co(2, 20, 1)[0]
            self.question_raw = Eq((x + a) ** 2, b)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            self.answer_raw = solve(self.question_raw)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_4_2_2(self):
        """Question MCAT 4.2.2 needs revision, produces to many of the same question (route 1: a = ...)"""

        self.question_description = "Solving exponential equations with unknowns in the base."

        if self.route is None:
            self.route = self.random_co(1, 3, 1)[0]

        if self.route == 1:
            x = symbols("x")
            power = self.random_co(3, 5, 1)[0]
            if power == 5:
                a = self.random_co(3, 3, 1)[0]
            else:
                a = self.random_co(3, power, 1)[0]
            self.question_raw = Eq(x ** power, a ** power)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            if power % 2 == 0:
                self.answer_raw = [a, -1 * a]
            else:
                self.answer_raw = a

        elif self.route == 2:
            x = symbols("x")
            soln = self.random_co(2, 5, 1)[0]
            power, multiple = self.random_co(3, 6, 2)
            adder = self.random_co(3, 20, 1)[0]
            self.question_raw = Eq(multiple * (x ** power) + adder, (soln ** power) * multiple + adder)
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            if power % 2 == 0:
                self.answer_raw = [soln, -1 * soln]
            else:
                self.answer_raw = soln

        else:
            x = symbols("x")
            c, power, soln = self.random_co(2, 6, 3)
            self.question_raw = Eq(c * (soln ** power), c * (x ** power))
            self.question_aspects = [r'&\text{Solve: }', '&' + latex(self.question_raw)]
            if power % 2 == 0:
                self.answer_raw = [soln, -1 * soln]
            else:
                self.answer_raw = soln

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_5_1_1(self):
        """Question MCAT 5.1.1"""

        self.question_description = "Solve simultaneous equations by elimination."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        elif self.route == 1:
            # Coefficients on y term are additive inverses of one another. (Adding equations to solve)

            x, y = symbols("x y")
            a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)

            xsoln = Rational((c + e), (a + d))
            ysoln = Rational((c * d - a * e), (b * (a + d)))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)
                xsoln = Rational((c + e), (a + d))
                ysoln = Rational((c * d - a * e), (b * (a + d)))

            eqn1 = Eq(a * x + b * y, c)
            eqn2 = Eq(d * x - b * y, e)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\'
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

        elif self.route == 2:
            # Coefficients on x are additive inverses of one another. (Adding equations to solve)

            x, y = symbols("x y")
            a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)

            xsoln = Rational((c * d - b * e), a * (b + d))
            ysoln = Rational((c + e), (b + d))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)
                xsoln = Rational((c * d - b * e), a * (b + d))
                ysoln = Rational((c + e), (b + d))

            eqn1 = Eq(a * x + b * y, c)
            eqn2 = Eq(-1 * a * x + d * y, e)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\'
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

        elif self.route == 3:
            # Coefficients on x are equal. (Subtracting equations to solve)

            x, y = symbols("x y")
            a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)

            xsoln = Rational((b * e - c * d), (a * (b - d)))
            ysoln = Rational((c - e), (b - d))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)
                xsoln = Rational((b * e - c * d), (a * (b - d)))
                ysoln = Rational((c - e), (b - d))

            eqn1 = Eq(a * x + b * y, c)
            eqn2 = Eq(a * x + d * y, e)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\'
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

        elif self.route == 4:
            # Coefficients on y are equal. (Subtracting equations to solve)

            x, y = symbols("x y")
            a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)

            xsoln = Rational((c - e), (a - d))
            ysoln = Rational((a * e - c * d), (b * (a - d)))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d, e = self.random_co(-6, 6, 5, zero=False)
                xsoln = Rational((c - e), (a - d))
                ysoln = Rational((a * e - c * d), (b * (a - d)))

            eqn1 = Eq(a * x + b * y, c)
            eqn2 = Eq(d * x + b * y, e)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\' 
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

        self.answer_aspects = [latex(self.answer_raw)]

    def generate_question_mcat_5_1_3(self):
        """MCAT Question 5.1.3"""

        self.question_description = "Solving simultaneous equations by substitution."

        if self.route is None:
            self.route = self.random_co(1, 2, 1)[0]

        self.route = 2

        if self.route == 1:
            x, y = symbols("x y")
            a, b, c, d, e = self.random_co(-8, 8, 5, zero=False)
            xsoln = Rational((e - b * d), (a * d + c))
            ysoln = Rational((a * e + b * c), (a * d + c))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d, e = self.random_co(-8, 8, 5, zero=False)
                xsoln = Rational((e - b * d), (a * d + c))
                ysoln = Rational((a * e + b * c), (a * d + c))

            eqn1 = Eq(y, a * x + b)
            eqn2 = Eq(c * x + d * y, e)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\'
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

        if self.route == 2:
            x, y = symbols("x y")
            a, b, c, d = self.random_co(-8, 8, 4, zero=False)
            xsoln = Rational((d - b), (a - c))
            ysoln = Rational((a * d - b * c), (a - c))

            while type(xsoln) and type(ysoln) is not Integer:
                a, b, c, d = self.random_co(-8, 8, 4, zero=False)
                xsoln = Rational((d - b), (a - c))
                ysoln = Rational((a * d - b * c), (a - c))

            eqn1 = Eq(y, a * x + b)
            eqn2 = Eq(y, c * x + d)

            self.question_aspects = [r'\text{Find } x,y \text{ such that }',
                                     r'\begin{array}{ccc}'
                                     r'&' + latex(eqn1) + r'\\'
                                     r'&' + latex(eqn2),
                                     r'\end{array}']

            self.answer_raw = (xsoln, ysoln)

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


def testing_repetition(question):
    init_printing()
    
    while True:
        new_question = MathsQuestion()
        new_question.generate_question(question)
        print(new_question.route)
        print(new_question.question_raw)
        print(new_question.question_aspects)
        print(new_question.answer_raw)
        print(new_question.answer_aspects)
        input()


if __name__ == "__main__":
    #testing()
    testing_repetition('5.1.3')
