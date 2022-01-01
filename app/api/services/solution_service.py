from sympy import solve, symbols
from sympy.parsing.latex import LaTeXParsingError, parse_latex

from app.api.helpers.errors import HttpError
from app.api.models.dto.attempt_response import AttemptResponse
from app.api.services.question_service import is_question, get_question


def check_solution(question_type, question_id, attempt, seed):

    if not is_question(question_type, question_id):
        raise HttpError(description=f"Question {question_type} {question_id} not found.",
                        status=404)

    # question = attempt.get("question")
    question_attempt = attempt.get("attempt")
    # independent_var = attempt.get("independent_var", "x")
    # is_attempt_correct = is_correct(question, question_attempt, independent_var)
    question = get_question(question_type, question_id, seed)
    return question.validate_attempt(question_attempt)


    # return AttemptResponse(question, question_attempt, is_attempt_correct), 200


def is_correct(question, attempt, independent_var="x"):
    # This method will certainly grow in complexity to handle other problem types
    # Could use question_type and question_id to help with knowing how to handle the solving

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
