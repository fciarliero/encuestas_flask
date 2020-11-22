from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse

from app import app, db
from app.forms import QuestionForm, SurveyForm, LoginForm, SignUpForm, MakePollForm, MakeQuestionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Poll, Question, Answer
from datetime import date

@app.route('/')
@app.route('/home')
def home():
    polls = Poll.query.filter(Poll.expiration > date.today()).all()
    return render_template('home.html', title='polls', polls=polls)


def get_option_list(question):
    options = []
    if question.option1 != '':
        options.append((question.option1, question.option1))
    if question.option2 != '':
        options.append((question.option2, question.option2))
    if question.option3 != '':
        options.append((question.option3, question.option3))
    if question.option4 != '':
        options.append((question.option4, question.option4))
    return options


def save_answer(form, poll_id):
    for answer in form.select_entries.data:
        question = Question.query.filter_by(id=answer['question']).first()
        submitted_answer = Answer(answerer=current_user, src_question=question, result=answer['option'])
        db.session.add(submitted_answer)
        db.session.commit()


@app.route('/poll/<id>', methods=['GET', 'POST'])
@app.route('/poll')
def poll(id):
    form = SurveyForm()
    current_poll = Poll.query.filter_by(id=id).first()
    if current_poll:
        if request.method == "POST":
            save_answer(form, id)
            flash('Poll Answer submitted')
            return redirect(url_for('home'))
        else:
            questions = Question.query.filter_by(parent=id).all()
            for question in questions:
                form.select_entries.append_entry()
                option_list = get_option_list(question)
                form.select_entries[-1].option.choices = option_list
                form.select_entries[-1].option.label = question.name
                form.select_entries[-1]['question'].data = question.id
            return render_template('survey.html', form=form, title=current_poll.name)
    else:
        print('no hay poll')


@app.route('/new_poll', methods=['GET', 'POST'])
@login_required
def new_poll():
    form = MakePollForm()
    if request.method == "POST" and form.validate_on_submit():
        poll = Poll(author=current_user, name=form.name.data,expiration=form.expiration.data)
        db.session.add(poll)
        db.session.commit()
        flash('Poll added, now add questions')
        return redirect(url_for('add_questions', poll_id=poll.id))
    return render_template('new_poll.html', title='create', form=form)


@app.route('/add_questions/<poll_id>', methods=['GET', 'POST'])
@app.route('/add_questions')
@login_required
def add_questions(poll_id):
    current_poll = Poll.query.filter_by(author=current_user,id=poll_id).first()
    form = MakeQuestionForm()
    if current_poll:
        questions = Question.query.filter_by(parent=poll_id).all()
        if form.validate_on_submit():
            question = Question(mother=current_poll, name=form.name.data, option1=form.option1.data,
                                option2=form.option2.data, option3=form.option3.data, option4=form.option4.data,
                                correct_answer=form.data[form.correct_answer.data])
            db.session.add(question)
            db.session.commit()
            flash('Question added!')
            return redirect(url_for('add_questions', poll_id=poll_id))
        return render_template('add_question.html', title='Add A Question', form=form, questions=questions)
    else:
        #error
        print('poll not found, F.')
        pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #esta parte hace que si te logueas despues de ir a un url con login required, vuelvas a el
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)
