from flask import Flask, render_template, g

from src.api.ncea_level_1.maths import mcat

app = Flask(__name__)


@app.route('/question/<string:question_number>')
def quiz_applet(question_number):
    new_question = mcat.MathsQuestion()

    new_question.generate_question(question_number)

    question = new_question.question_aspects
    g.question_len = range(len(question))

    for itt in g.question_len:
        question[itt] = question[itt].replace("&", "")

    g.question = question


    return render_template('quiz_applet.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
