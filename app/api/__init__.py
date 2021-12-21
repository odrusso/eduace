from time import time
from flask import Flask, request

from app.api.helpers.config import API_VERSION, CORS_ALLOWED_ORIGINS, DEBUG
from app.api.helpers.errors import HttpError
from app.api.services.question_service import get_all_questions, get_question
from app.api.services.solution_service import check_solution

app = Flask(__name__)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = CORS_ALLOWED_ORIGINS

    return response

@app.get(API_VERSION + "/question/<question_type>/<question_id>")
def question_router(question_type, question_id):
    seed = int(request.args.get("seed", time()))
    question, status = get_question(question_type, question_id, seed)

    return question.json, status

@app.post(API_VERSION + "/question/<question_type>/<question_id>")
def get_solution(question_type, question_id):
    attempt = request.get_json(force=True)
    attempt_response, status = check_solution(question_type, question_id, attempt)

    return attempt_response.json, status

@app.get(API_VERSION + "/questions")
def questions():
    question_dict, status = get_all_questions()

    return question_dict, status

@app.errorhandler(HttpError)
def handle_http_error(error):

    return error.json, error.json.get("status", 500)

if __name__ == "__main__":
    app.run(debug=DEBUG)
