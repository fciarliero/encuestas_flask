from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import QuestionForm, SurveyForm, LoginForm, SignUpForm


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
    form = QuestionForm()
    form.options.choices = [(1,'papa'),(2,'op2')]
    form2 = SurveyForm()
    for x in range(10):
        form2.select_entries.append_entry()
    for subform in form2.select_entries:
        subform.options.choices=[(1, 'papfaa'), (2, 'opaf2')]
        subform.options.label='chupala putito'
    return render_template('survey.html', form = form2)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session.pop('user_id', None)
    if request.method == 'POST' and form.validate_on_submit():
        session['user_id'] = form.user.data
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        session['user_id'] = form.user.data
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
