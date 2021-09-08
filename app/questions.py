from .question_factory import QUESTION_MAPPING
from .utils import is_question


class QuestionNotFound(Exception):
    def __init__(self):
        self.description = "Question not found."

    @property
    def json(self):
        return {
            "description": self.description,
        }


def get_question(question_type, question_id, seed):

    if is_question(question_type, question_id):
        question = QUESTION_MAPPING.get(question_type).get(question_id)(seed)
        status = 200

        return question, status

    else:
        raise QuestionNotFound


def get_all_questions():
    question_response = {"questions": []}

    for question_type, question_type_items in QUESTION_MAPPING.items():
        question_response["questions"].append({
            "questionTypeName": question_type,
            "questionIds": list(question_type_items.keys())
        })

    return question_response, 200
