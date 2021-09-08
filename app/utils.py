from . import questions
from .question_factory import QUESTION_MAPPING


def is_question(question_type, question_id):

    valid_type = QUESTION_MAPPING.get(question_type, False)

    return valid_type.get(question_id, False) if valid_type else False
