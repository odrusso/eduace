def generate_question_factor_1(self):
    x, y = symbols("x y")
    xa, xb = self.random_co(-8, 8, 2)
    self.answer_raw = (x + xa) * (x + xb)
    self.question_raw = expand(self.answer_raw)
    line1 = ["A", data.choose(data.context_options), "has an area of", str(self.question_raw)]
    line2 = ["What are the lengths of the sides in terms of x?"]
    self.question_aspects = [line1, line2]


def generate_question_factor_2(self):
    x, y = symbols("x y")
    xa, xb = self.random_co(-8, 8, 2)
    self.answer_raw = (x + xa) * (x + xb)
    self.question_raw = expand(self.answer_raw)
    self.answer_raw = (x + xb)
    line1 = ["A", data.choose(data.context_options), "has an area of", str(self.question_raw)]
    line2 = ["One side can be described as", str((x + xa))]
    line3 = ["What are the lengths of the sides in terms of x?"]
    self.question_aspects = [line1, line2, line3]


def generate_question_quadratic_solve(self):
    x, y = symbols("x y")
    xa, xb = self.random_co(-8, 8, 2)
    xc = self.random_co(2, 4, 1)[0]
    answer_backwards = (xc * x + xa) * (x + xb)
    self.question_raw = expand(answer_backwards)
    self.answer_raw = solve(self.question_raw)
    self.question_aspects = [["Solve", self.question_raw]]
    self.answer_aspects = [answer_backwards, self.answer_raw]


def generate_question_quote_sim(self):
    x = symbols("x")
    xa, xb, xc, xd = self.random_co(-5, 5, 4)
    self.answer_raw = (x + xa) / (xb * x)
    self.question_raw = expand((x + xa) * (x + xc)) / expand((x + xc) * (xb * x))
    self.question_aspects = [["Simplify", self.question_raw]]
    self.answer_aspects = [["Factorise", str((x + xa) * (x + xc) / (x + xc) * (xb * x))], [self.answer_raw]]


def generate_question_quote_solve(self):
    """WARNING: HIGHLY UNOPTIMISED"""
    x = symbols("x")

    xa, xb = self.random_co(-10, 10, 2)
    xc, xd = self.random_co(0, 6, 2)

    while sqrt(xc * xd).is_integer():
        xc, xd = self.random_co(0, 6, 2)

    xb, xc, xd, xe = self.random_co(-7, 7, 4)
    self.question_raw = Eq(expand((x + xa) * (x + xb)) / ((x + xa) * (x + xc)), (x / xd))
    self.answer_raw = solve(self.question_raw)
    self.answer_aspects = [["x =", str(self.answer_raw)]]
    self.question_aspects = [["Solve", self.question_raw]]