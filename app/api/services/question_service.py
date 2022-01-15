from app.api.models.questions_mcat import MCATQuestion1, MCATQuestion2, MCATQuestion3

QUESTION_MAPPING = {
    'mcat': {
        '1': MCATQuestion1,
        '2': MCATQuestion2,
        '3': MCATQuestion3
    },
}


def get_question(question_type, question_id, seed):

    return QUESTION_MAPPING.get(question_type).get(question_id)(seed)


def get_question_latex(question_type, question_id, seed):

    return get_question(question_type, question_id, seed).question


def get_all_questions():
    all_questions = []

    mcat_questions = QUESTION_MAPPING["mcat"]
    for question_id, question_object in mcat_questions.items():
        all_questions.append(
                {
                    "id": question_id,
                    "typeName": "mcat",
                    "description": question_object.description
                }
        )

    return all_questions


def is_question(question_type, question_id):

    valid_type = QUESTION_MAPPING.get(question_type, False)

    return valid_type.get(question_id, False) if valid_type else False
