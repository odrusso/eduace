from time import time
from flask import Flask, request, abort

from app.api.helpers.config import API_VERSION, CORS_ALLOWED_ORIGINS, DEBUG, PORT, GIT_HASH
from app.api.helpers.errors import HttpError
from app.api.services.question_service import get_all_questions, get_question_latex, is_question
from app.api.services.solution_service import check_solution

app = Flask(__name__)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = CORS_ALLOWED_ORIGINS

    return response


@app.get("/api/version")
def controller_api_version():
    return GIT_HASH


@app.get(API_VERSION + "/question/<question_type>/<question_id>")
def controller_get_question(question_type, question_id):
    seed = int(request.args.get("seed", time()))

    if not is_question(question_type, question_id):
        abort(404)

    question = get_question_latex(question_type, question_id, seed)

    return {'question': question, 'seed': seed}, 200


@app.post(API_VERSION + "/question/<question_type>/<question_id>")
def controller_validate_question_solution(question_type, question_id):
    attempt = request.get_json(force=True)
    seed = attempt.get("seed")
    attempt_latex = attempt.get("attempt")

    if not is_question(question_type, question_id):
        abort(404)

    attempt_response = check_solution(question_type, question_id, attempt_latex, seed)

    return {'result': attempt_response}, 200


@app.get(API_VERSION + "/questions")
def controller_get_all_questions():
    return get_all_questions(), 200


@app.errorhandler(HttpError)
def handle_http_error(error):
    return error.json, error.json.get("status", 500)


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)
