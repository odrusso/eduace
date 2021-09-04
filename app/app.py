from flask import Flask, request
from .config import API_VERSION
from time import time
from .questions import get_question

app = Flask(__name__)

@app.route(API_VERSION + "/question/<question_type>/<question_id>", methods=["GET"])
def question_router(question_type, question_id):

    seed = request.args.get("seed", time())
    question, status = get_question(question_type, question_id, seed)

    return question.json, status


if __name__ == "__main__":
    app.run(debug=True)