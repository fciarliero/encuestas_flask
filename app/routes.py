from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import  Question, Survey


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
@app.route('/poll')
def poll():
    form = Question()
    form.options.choices = [(1,'papa'),(2,'op2')]
    form2 = Survey()
    for x in range(10):
        form2.select_entries.append_entry()
    for subform in form2.select_entries:
        subform.options.choices=[(1, 'papfaa'), (2, 'opaf2')]
        subform.options.label='chupala putito'
    return render_template('survey.html', form = form2)