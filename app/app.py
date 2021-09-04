from flask import Flask, request
from .services import mcat

app = Flask(__name__)

QUESTION_TYPE_MAPPING = {
    'mcat': mcat,
}

@app.route("/question/<question_type>/<question_id>", methods=["GET"])
def question_router(question_type, question_id=None):

    if question_class := QUESTION_TYPE_MAPPING.get(question_type, ""):
        seed = request.args.get("seed", "")
        question = question_class(question_id, seed)

    return question

if __name__ == "__main__":
    app.run(debug=True)