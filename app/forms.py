from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User


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


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError('Wrong username or password.')
        else:
            pass


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_pass = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')