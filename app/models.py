from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    polls = db.relationship('Poll', backref='author', lazy='dynamic')
    question_answers = db.relationship('Answer', backref='answerer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expiration = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Question', backref='mother', lazy='dynamic')

    def __repr__(self):
        return '<Poll {}>'.format(self.name)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    option1 = db.Column(db.String(128))
    option2 = db.Column(db.String(128))
    option3 = db.Column(db.String(128))
    option4 = db.Column(db.String(128))
    correct_answer = db.Column(db.String(128))
    parent = db.Column(db.Integer, db.ForeignKey('poll.id'))
    answers = db.relationship('Answer', backref='src_question', lazy='dynamic')
        #db.Column(db.Integer, db.ForeignKey('answer.id'))

    def __repr__(self):
        return '<Question {}>'.format(self.name)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    result = db.Column(db.String(128))

    def __repr__(self):
        return '<Answer {}>'.format(self.result)