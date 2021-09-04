import sys
from sympy import symbols, latex, Eq, Rational

QUESTIONS = {
    'mcat': set(
        '1',
    ),
}

def get_question(question_id, question_type, seed):
    """Mildy dodgy"""
    return getattr(sys.modules[__name__], question_type + "_" + question_id)(seed)


def mcat_1(seed):
    x = symbols('x')
    ## TODO: use the seed
    a = 2
    b = 3

    question = Eq(a * x + b, 0)
    solution = Eq(x, -1 * Rational(b, a))

    return {
        "description": "Solve a linear equation.",
        "question_latex": latex(question),
        "solution_latex": latex(solution),
    }
