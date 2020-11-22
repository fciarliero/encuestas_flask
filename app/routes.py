from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse

from app import app, db
from app.forms import QuestionForm, SurveyForm, LoginForm, SignUpForm, MakePollForm, MakeQuestionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Poll, Question
from datetime import date

@app.route('/')
@app.route('/home')
def home():
    polls = Poll.query.filter(Poll.expiration > date.today()).all()
    return render_template('home.html', title='polls', polls=polls)


@app.route('/poll/<id>', methods=['GET', 'POST'])
@app.route('/poll')
def poll(id):
    hola = id
    form2 = SurveyForm()
    for x in range(10):
        form2.select_entries.append_entry()
    for subform in form2.select_entries:
        subform.options.choices=[(1, 'papfaa'), (2, 'opaf2')]
        subform.options.label='chupala putito'
    return render_template('survey.html', form = form2)


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
                                correct_answer=form.correct_answer.data)
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
