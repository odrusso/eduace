from flask import Flask, render_template, g, jsonify, request

from src.api.ncea_level_1.maths import mcat

app = Flask(__name__)

GLOBALS = {}

@app.route('/question/')
def applet_selection():

    g.include_bootstrap = r"""<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
        <script src="https://unpkg.com/popper.js/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>"""

    return render_template("selection.html")

@app.route('/question/<string:question_number>')
def quiz_applet(question_number):
    GLOBALS["question"] = mcat.MathsQuestion()

    GLOBALS["question"].generate_question(question_number)

    question = GLOBALS["question"].question_aspects

    g.question_len = range(len(question))

    for itt in g.question_len:
        question[itt] = question[itt].replace("&", "")

    g.question = question

    g.answer = GLOBALS["question"].answer_aspects[0]

    g.route = GLOBALS['question'].route

    g.question_number = question_number


    g.include_latex = r"""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.0-alpha/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.10.0-alpha/dist/katex.min.js"></script>
        """

    g.include_bootstrap = r"""<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
        <script src="https://unpkg.com/popper.js/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>"""

    g.include_mathquill = r"""<link rel="stylesheet" href="http://mathquill.com/lib/mathquill.css"/>
    <script src="http://mathquill.com/lib/mathquill.js"></script>
    <script>
    var MQ = MathQuill.getInterface(2);
    </script>"""

    return render_template('quiz_applet.html')

@app.route("/question/_evaluate_answer")
def evaluate_answer():
    entered_answer = request.args.get("entered_latex")

    return jsonify(result=GLOBALS["question"].evaluate_answer(entered_answer))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
