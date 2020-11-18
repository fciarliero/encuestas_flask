from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired


class QuestionForm(Form):
    options = SelectField(label=u'Pregunta?', coerce=int)


class SurveyForm(FlaskForm):
    select_entries = FieldList(FormField(QuestionForm))
    submit = SubmitField('Answer')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repat_pass = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')