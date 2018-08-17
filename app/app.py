"""
 ___   ___    _   _     _      ___   ___
| __| |   \  | | | |   /_\    / __| | __|
| _|  | |) | | |_| |  / _ \  | (__  | _|
|___| |___/   \___/  /_/ \_\  \___| |___|

Main Web App

Python 3.6.5
Written by EduAce NZ

"""

# Dependency  Imports
from flask import Flask, render_template, g, jsonify, request, redirect, abort, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from sqlalchemy import exc
from time import time, strftime, gmtime
from itsdangerous import URLSafeSerializer
from raven.contrib.flask import Sentry
import json
import pickle
import operator

# Internal Imports
from data_abstract import *
from config import SECRET_KEY, MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, SENTRY_URL, HOST, DEBUG


application = app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False

mail = Mail(app)
login_manager = LoginManager(app)
email_serialiser = URLSafeSerializer(app.config["SECRET_KEY"])

sentry = Sentry(app, dsn=SENTRY_URL)


class User(UserMixin):
    def __init__(self, id):
        self.id = int(id)
        self.datauser = get_user_from_id(self.id)
        # user_db = sqlite3.connect('data/users.db')
        # database_user = user_db.cursor().execute("""SELECT * FROM `Users` WHERE `id`=?""", (id,)).fetchone()
        # user_db.close()
        self.username = self.datauser.username
        self.email = self.datauser.email
        self.role = self.datauser.role
        self.score = self.datauser.score

@login_manager.user_loader
def load_user(id):
    return User(id)


@app.route("/")
def web_index():
    return render_template("index.html")


@app.route("/login")
def web_login():
    if current_user.is_anonymous:
        return render_template("login.html", failure='None')
    else:
        return redirect('/dashboard')


@app.route('/login', methods=['POST'])
@app.route('/confirm_email/<token>', methods=['POST'])
def verify_login(token=None):
    username = request.form['username']
    password = request.form['password']
    result = pull_user(username, password)
    if result[0]:
        user_id = result[1]
        login_user(load_user(user_id))
        return redirect("/dashboard")
    elif result[1] == 'username':
        return render_template("/login.html", failure="username")  # failure state required
    elif result[1] == 'unconfirmed':
        # send another email
        return render_template("/login.html", failure="unconfirmed")  # failure state required
    else:
        return render_template("/login.html", failure="password")  # failure state required


@app.route("/_logout")
@login_required
def user_logout():
    logout_user()
    return redirect("/")


@app.route("/dashboard")
@login_required
def web_dashboard():
    # strftime("%d/%m/%y %H:%M", gmtime(time()))
    if len(current_user.datauser.question_structures.all()) == 0:
        return render_template("dashboard_fresh.html")
    else:
        course_name = "MCAT"
        
        structure_id = current_user.datauser.active_structure

        correct_questions = current_user.datauser.current_questions_correct
        correct_questions_improvement = current_user.datauser.current_questions_correct >= current_user.datauser.last_questions_correct
        if current_user.datauser.current_questions_correct + current_user.datauser.current_questions_incorrect == 0:
            correct_percent = 0
        else:
            correct_percent = (100 * current_user.datauser.current_questions_correct) / (current_user.datauser.current_questions_correct + current_user.datauser.current_questions_incorrect)
        if correct_percent == 0:
            correct_percent_improvement = False
        elif current_user.datauser.last_questions_correct + current_user.datauser.last_questions_incorrect == 0:
            correct_percent_improvement = True
        else:
            correct_percent_improvement = correct_percent > (100 * current_user.datauser.last_questions_correct) / (current_user.datauser.last_questions_correct + current_user.datauser.last_questions_incorrect)

        no_of_questions = len(session.query(DataQuestion).filter(DataQuestion.question_structure_id==structure_id).all())
        if no_of_questions == 0:
            module_percent = 0
        else:
            module_percent = 100 * session.query(DataQuestionStructure).filter(DataQuestionStructure.question_structure_id==structure_id).first().questions_correct / no_of_questions

        return render_template('dashboard.html', 
                                correct_questions=correct_questions,
                                correct_questions_improvement=correct_questions_improvement,
                                correct_percent="{0:.1f}".format(correct_percent),
                                correct_percent_improvement=correct_percent_improvement,
                                module_percent="{0:.1f}".format(module_percent),
                                structure_recent=structure_id)

@app.route("/quiz/<string:question_structure_number>")
@login_required
def web_quiz(question_structure_number):
    current_structure_object = current_user.datauser.question_structures.filter_by(question_structure_id=question_structure_number).first()
    if current_structure_object is None:
        abort(404)
    else:
        current_question_list = current_structure_object.questions.all()
        sidebar_question_list = []
        for data_question_object in current_question_list:
            current = []
            current.append(data_question_object.question_id)
            current.append(data_question_object.question_structure_itt)
            current.append(data_question_object.question_description)
            current.append(data_question_object.get_question_status())
            sidebar_question_list.append(current)

        sidebar_question_list = sorted(sidebar_question_list, key=operator.itemgetter(1))

        current_structure_object.recent_access = time()
        session.commit()

        return render_template("quiz.html", sidebar_question_list=sidebar_question_list, current_question=current_structure_object.current_question)


@app.route("/quiz/_load_question_json")
@login_required
def load_question_json():
    question_id = request.args.get("question_id")
    data_question_object = session.query(DataQuestion).filter(DataQuestion.question_id == question_id).first()

    data_question_object.structure.current_question = question_id
    session.commit()

    question = pickle.loads(data_question_object.question_pickle)

    if type(question.answer_raw) == type([1, 2]):
        answer_length = len(question.answer_raw)
    else:
        answer_length = 1

    recent_answer = data_question_object.get_recent_answer()

    return jsonify(question_latex=question.question_aspects, answer_length=answer_length, recent_answer=recent_answer)


@app.route("/quiz/_evaluate_answer")
@login_required
def evaluate_answer():
    entered_answer = request.args.get("entered_answers")
    entered_answer = json.loads(entered_answer)
    question_id = request.args.get("question_id")
    data_question = session.query(DataQuestion).filter(DataQuestion.question_id == question_id).first()
    question = pickle.loads(data_question.question_pickle)
    correct = question.evaluate_answer(entered_answer)
    answer = DataAnswer(question_id=question_id,
                        answer_pickle=pickle.dumps(entered_answer),
                        time_entered=time(),
                        timer_current=0,
                        correct= False not in correct)
    session.add(answer)
    
    if answer.correct:
        data_question.correct = 1
        current_user.datauser.current_questions_correct += 1
        data_question.structure.questions_correct += 1
    else:
        current_user.datauser.current_questions_incorrect += 1
        data_question.structure.questions_incorrect += 1

    session.commit()

    return jsonify(result=str(data_question.correct))


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        username_exists = len(session.query(DataUser.username).filter_by(username=request.form['username']).all()) != 0
        email_exists = len(session.query(DataUser.username).filter_by(email=request.form['email']).all()) != 0
        password = request.form['password']

        if username_exists:
            return render_template("register.html", error="Username already exists!")

        elif email_exists:
            return render_template("register.html", error="Email already exists!")

        elif len(password) < 8:
            return render_template("register.html", error="Password must be greater than 8 characters!")

        else:

            confirm_token = email_serialiser.dumps(request.form["email"], salt="email-confirm")
            confirm_message = Message("Confirm Email", sender="it@eduace.co.nz", recipients=[request.form["email"]])
            confirm_link = url_for("confirm_email", token=confirm_token, _external=True)
            confirm_message.body = "Confirm: <a>%s</a>" % confirm_link

            mail.send(confirm_message)

            new_user = DataUser(username=request.form['username'], 
                                passhash=generate_password_hash(password),
                                email=request.form["email"], 
                                confirmed=False, 
                                role="demo", 
                                score=0,
                                last_questions_correct=0,
                                last_questions_incorrect=0,
                                current_questions_incorrect=0,
                                current_questions_correct=0,
                                active_structure=0 
                                )
            session.add(new_user)
            session.commit()

            return render_template("register_success.html")
    else:
        if not current_user.is_anonymous:
            return redirect('/dashboard')
        else:
            return render_template("register.html", error="")


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = email_serialiser.loads(token, salt="email-confirm")
        confirm_email_update(email)
        return render_template("/login.html", failure="confirmed")
    except:
        return "<h1>Invalid confirmation</h1>"


@app.route("/register_success.html")
def testingbla():
    return render_template("register_success.html")


@app.route("/_generate_mcat_exam")
def generate_demo_exam():
    generate(current_user.id)
    return redirect('/dashboard')


@app.route("/careers")
def pointless():
    return "Uhh - you found an easter egg! But unfortunately we don't even make enough money to pay our own developers, let alone hire anyone :/ <br> If you're super keen to get involved, you could chuck it@eduace.co.nz an email :)"

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/error.html', refresh=redirect(request.url), error=e, error_short=str(e).split(":")[0]), 404

@app.errorhandler(exc.InvalidRequestError)
@app.errorhandler(exc.OperationalError)
@app.errorhandler(exc.InterfaceError)
@app.errorhandler(exc.TimeoutError)
def handle_invalid_sql_request(e):
    session.rollbal()
    session = return_session()
    print("Session has been rolled-back after error has occured")
    return redirect(request.url)

#@app.errorhandler(AttributeError)
def handle_invalid_data(e):
    session.rollbal()
    session = return_session()
    print("Page has been forced reset due to an AttributeError")
    return redirect(request.url)

@app.route("/test")
def test():
    return render_template("/dashboard.html")

if __name__ == '__main__':
    app.run(host=HOST, debug=DEBUG)
