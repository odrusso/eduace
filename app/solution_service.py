from sympy.parsing.latex import parse_latex
from sympy import symbols, solve

def is_correct(question, attempt):
    ## This method will certainly grow in complexity to handle other
    ## problem types

    x = symbols("x")

    question_expr = solve(parse_latex(question), x)
    attempt_expr = solve(parse_latex(attempt), x)

    return question_expr == attempt_expr