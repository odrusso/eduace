from sympy import solve, symbols
from sympy.parsing.latex import LaTeXParsingError, parse_latex

from .errors import HttpError


def is_correct(question, attempt, question_type, question_id, independent_var="x"):
    ## This method will certainly grow in complexity to handle other
    ## problem types
    ## Could use question_type and question_id to help with knowing how to handle the solving

    var = symbols(independent_var)

    try:
        question_expr = solve(parse_latex(question), var)
        attempt_expr = solve(parse_latex(attempt), var)

    except LaTeXParsingError:
        raise HttpError(description="Error parsing LaTeX input.",
                        status=400)

    return question_expr == attempt_expr
