from app.api.services.question_service import get_question


def check_solution(question_type, question_id, attempt_latex, seed):
    # This method requires that both question_type and question_id have already been validated
    question = get_question(question_type, question_id, seed)
    return question.validate_attempt(attempt_latex)
