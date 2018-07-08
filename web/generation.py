# Dependency  Imports
from flask import Flask, render_template, g, jsonify, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import pickle
import operator
from time import time
import sys

# Internal Imports
sys.path.append('.')
sys.path.append('./enviroment/lib/python3.6/site-packages')


from src.courses import course_master
from src.courses.ncea_level_1.maths import mcat
from data_abstract import *

def generate(user_id):

    MATHS_QUESTION_LIST = ["1.1.2", "1.1.2", "1.1.3", "1.1.4", "1.2.1", "1.2.2", "1.3.1", "1.3.2", "1.3.3", "1.3.4"]

    new_question_structure = DataQuestionStructure(user_id=user_id, time_generated=int(time()))

    session.add(new_question_structure)

    session.commit()

    st_id = new_question_structure.question_structure_id

    session.query(DataUser).filter(DataUser.user_id == user_id).one().current_structure = st_id

    print(st_id)

    itt = 0
    for question in MATHS_QUESTION_LIST:
        question_object = mcat.MathsQuestion(question)
        print(question_object)
        data_question_object = DataQuestion(question_pointer = "courses.ncea_level_1.maths.%s" % question,
                                            question_pickle=pickle.dumps(question_object),
                                            question_structure_itt=itt,
                                            question_structure_id=st_id,
                                            time_gen=int(time())
                                            )
        session.add(data_question_object)

    new_question_structure.current_question = data_question_object.question_id

    session.commit()
