# utf-8
# Python 3.6, SymPy 1.1.1
# http://github.com/odrusso/eduace

# External Imports
from sqlalchemy import create_engine, Column, ForeignKey, INTEGER, String, BLOB, FLOAT, Boolean
from sqlalchemy.exc import InternalError, StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

#Internal Imports
from application import app

Base = declarative_base()

def pull_user(username, password):
    """Returns [True, UserID] if the user exists, and the password is correct,
    returns [False, "username] if the user does not exist, and
    returns [False, "password"] if the user exists, but the password is incorrect"""
    user_result = session.query(DataUser).filter(DataUser.username==username).all()
    if len(user_result) == 0:
        return [False, "username"]
    else:
        current_user = user_result[0]
        if current_user.confirmed:
            if check_password_hash(current_user.passhash, password):
                return [True, current_user.user_id]
            else:
                return [False, "password"]
        else:
            return [False, "unconfirmed"]

def get_user_from_id(id):
    try:
        return session.query(DataUser).filter(DataUser.user_id==id).first()
    except InternalError:
        session.rollback()
        get_user_from_id(id)
    except StatementError:
        session.rollback()
        get_user_from_id(id)


def confirm_email_update(email):
    try:
        session.query(DataUser).filter(DataUser.email==email).first().confirmed = True
        session.commit()
    except:
        return None


class DataUser(Base):
    __tablename__ = 'users'

    user_id = Column(INTEGER, primary_key=True)
    username = Column(String)
    email = Column(String)
    passhash = Column(String)
    role = Column(String)
    score = Column(INTEGER)
    confirmed = Column(Boolean)

    question_structures = relationship("DataQuestionStructure", lazy='dynamic')

    institutes = relationship("DataInstitutes", lazy="dynamic")
    classes = relationship("DataClasses", lazy="dynamic")

    def __repr__(self):
        return "<User(user_id='%s', username='%s', email='%s', role='%s', score='%s')>" % (
            self.user_id, self.username, self.email, self.role, self.score)

    def __str__(self):
        return "%s: %s" % (self.user_id, self.username)


class DataQuestionStructure(Base):
    __tablename__ = 'question_structure'

    question_structure_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('users.user_id'))
    name = Column(String)
    time_generated = Column(FLOAT)
    time_completed = Column(FLOAT)
    recent_access = Column(FLOAT)
    current_question = Column(INTEGER)

    questions = relationship("DataQuestion", lazy='dynamic')

    def __repr__(self):
        return "<QuestionStructure(id='%s', length='%s')>" % (
            self.question_structure_id, self.length)

    def completion_percent(self):
        all_questions = self.questions.all()
        total = len(all_questions)
        correct = 0
        for question in all_questions:
            if question.correct:
                correct += 1
        #return "%s" % int(100*(correct/total+1))
        return "1"



class DataQuestion(Base):
    __tablename__ = 'questions'

    question_id = Column(INTEGER, primary_key=True)
    question_structure_id = Column(INTEGER, ForeignKey('question_structure.question_structure_id'))
    question_structure_itt = Column(INTEGER)
    question_pointer = Column(String)
    question_pickle = Column(BLOB)
    question_description = Column(String)
    time_gen = Column(INTEGER)
    time_init = Column(FLOAT)
    time_completed = Column(FLOAT)
    current_timer = Column(INTEGER)
    correct = Column(Boolean)

    structure = relationship("DataQuestionStructure", back_populates="questions")

    answers = relationship("DataAnswer", lazy='dynamic')

    def get_question_status(self):
        if len(self.answers.all()) == 0:
            return "unanswered"
        elif self.correct:
            return "correct"
        else:
            return "incorrect"

    def __repr__(self):
        return "<Question(id='%s')>" % self.question_id

    def get_recent_answer(self):
        if len(self.answers.all()) == 0:
            return ["", ""]
        else:
            return pickle.loads(self.answers.all()[-1].answer_pickle)

class DataAnswer(Base):
    __tablename__ = 'answers'

    answer_id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('questions.question_id'))
    answer_pickle = Column(BLOB)
    time_entered = Column(FLOAT)
    timer_current = Column(INTEGER)
    correct = Column(Boolean)

    def __repr__(self):
        return "<Answer(id='%s', completion='%s')>" % (self.answer_id, self.correct)


class DataInstitutes(Base):
    __tablename__ = 'institutes'

    institute_id = Column(INTEGER, primary_key=True)
    name = Column(String)
    leader_id = Column(INTEGER, ForeignKey('users.user_id'))

    classes = relationship("DataClasses", lazy="dynamic")
    leader = relationship("DataUser", back_populates="institutes")

    def __str__(self):
        return "Institute(id=%s, name=%s)" % (self.institute_id, self.name)


class DataClasses(Base):
    __tablename__ = 'classes'

    class_id = Column(INTEGER, primary_key=True)
    name = Column(String)
    leader_id = Column(INTEGER, ForeignKey('users.user_id'))
    institute_id = Column(INTEGER, ForeignKey('institutes.institute_id'))

    institute = relationship("DataInstitutes", back_populates="classes")
    leader = relationship("DataUser", back_populates="classes")


    def __str__(self):
        return "Class(id=%s, name=%s)" % (self.class_id, self.name)


engine = create_engine(app.config["DB_ENGINE"])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# print(__name__ + ": SQL Session Initialised")


if __name__ == "__main__":

    current_class = session.query(DataClasses).first()

    print(current_class)
    print(current_class.institute)
    print(current_class.leader)
    print(current_class.institute.leader)