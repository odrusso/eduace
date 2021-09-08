from sympy import solve, symbols
from sympy.parsing.latex import parse_latex


def is_correct(question, attempt, question_type, question_id, independent_var="x"):
    ## This method will certainly grow in complexity to handle other
    ## problem types
    ## Could use question_type and question_id to help with knowing how to handle the solving

    var = symbols(independent_var)

    question_expr = solve(parse_latex(question), var)
    attempt_expr = solve(parse_latex(attempt), var)

    return question_expr == attempt_expr
