from flask import Flask, request
from .config import API_VERSION
from time import time
from .questions import get_question, get_all_questions

app = Flask(__name__)

@app.route(API_VERSION + "/question/<question_type>/<question_id>", methods=["GET"])
def question_router(question_type, question_id):

    seed = int(request.args.get("seed", time()))
    question, status = get_question(question_type, question_id, seed)

    return question.json, status

@app.route(API_VERSION + "/questions", methods=["GET"])
def questions():
    
    question_dict, status = get_all_questions()

    return question_dict, status


if __name__ == "__main__":
    app.run(debug=True)
