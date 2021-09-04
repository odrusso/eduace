from flask import Flask, request
from .config import API_VERSION
from time import time
from .questions import get_question, get_all_questions
from .solutions import get_solution

app = Flask(__name__)

@app.route(API_VERSION + "/question/<question_type>/<question_id>", methods=["GET"])
def question_router(question_type, question_id):

    seed = request.args.get("seed", time())
    question, status = get_question(question_type, question_id, seed)

    return question.json, status

@app.route(API_VERSION + "/questions", methods=["GET"])
def questions():
    
    question_dict, status = get_all_questions()

    return question_dict, status

@app.route(API_VERSION + "/solution/<question_type>/<question_id>", methods=["POST"])
def solution_router(question_type, question_id):

    seed = request.args.get("seed", time())
    solution, status = get_solution(question_type, question_id, seed)

    return solution.json, status

if __name__ == "__main__":
    app.run(debug=True)
