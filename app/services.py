from time import time
from .questions import get_question
from .questions import QUESTIONS

def mcat(question_id, seed=time()):

    if question_id in QUESTIONS.get('mcat'):
        question = get_question(question_id, 'mcat', seed)

    return question
