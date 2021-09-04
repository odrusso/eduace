from flask import Flask, request
from time import time
from .questions import get_question

app = Flask(__name__)

@app.route("/question/<question_type>/<question_id>", methods=["GET"])
def question_router(question_type, question_id):

    seed = request.args.get("seed", time())
    question = get_question(question_type, question_id, seed)

    return question.json


if __name__ == "__main__":
    app.run(debug=True)