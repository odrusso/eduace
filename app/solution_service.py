from sympy import solve, symbols
from sympy.parsing.latex import LaTeXParsingError, parse_latex

from .errors import HttpError


def is_correct(question, attempt, question_type, question_id, independent_var="x"):
    ## This method will certainly grow in complexity to handle other
    ## problem types
    ## Could use question_type and question_id to help with knowing how to handle the solving

    var = symbols(independent_var)

    parsed_question = parse_latex(question)
    parsed_attempt = parse_latex(attempt)

    if parsed_question == parsed_attempt:
        return False

    try:
        question_expr = solve(parsed_question, var)
        attempt_expr = solve(parsed_attempt, var)

    except LaTeXParsingError as parsing_error:
        raise HttpError(description="Error parsing LaTeX input.",
                        status=400) from parsing_error

    return question_expr == attempt_expr
