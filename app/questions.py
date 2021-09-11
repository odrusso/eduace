from .errors import HttpError
from .question_factory import QUESTION_MAPPING
from .utils import is_question


def get_question(question_type, question_id, seed):

    if is_question(question_type, question_id):
        question = QUESTION_MAPPING.get(question_type).get(question_id)(seed)
        status = 200

    else:
        raise HttpError(description="Question not found.",
                        status=404)

    return question, status



def get_all_questions():
    question_response = {"questions": []}

    for question_type, question_type_items in QUESTION_MAPPING.items():
        question_response["questions"].append({
            "questionTypeName": question_type,
            "questionIds": list(question_type_items.keys())
        })

    return question_response, 200
