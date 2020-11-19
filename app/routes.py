from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse

from app import app, db
from app.forms import QuestionForm, SurveyForm, LoginForm, SignUpForm, MakePollForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('home.html', title='Home', user=user, posts=posts)


@app.route('/poll', methods=['GET', 'POST'])
def poll():
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
    if form.validate_on_submit():
        #agregar a la base de datos el prototipo de poll
        #redireccionar a la pagina de adicion de questions
        pass
    return render_template('new_poll.html', title='create', form=form)


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
