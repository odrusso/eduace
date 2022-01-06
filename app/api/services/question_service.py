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
    question_response = {"questions": []}

    for question_type, question_type_items in QUESTION_MAPPING.items():
        question_response["questions"].append({
            "questionTypeName": question_type,
            "questionIds": list(question_type_items.keys())
        })

    return question_response


def is_question(question_type, question_id):

    valid_type = QUESTION_MAPPING.get(question_type, False)

    return valid_type.get(question_id, False) if valid_type else False
