from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app.models import User
from datetime import date

class QuestionForm(Form):
    options = SelectField(label=u'Pregunta?', coerce=int)


class SurveyForm(FlaskForm):
    select_entries = FieldList(FormField(QuestionForm))
    submit = SubmitField('Answer')


class MakeQuestionForm(Form):
    name = StringField('Question:', validators=[DataRequired()])
    option1 = StringField('Option 1:')
    option2 = StringField('Option 2:')
    option3 = StringField('Option 3:')
    option4 = StringField('Option 4:')
    submit = SubmitField('Add Question')

    def validate_option1(self, option1):
        if self.option1 is None and self.option2 is None and self.option3 is None and self.option4 is None:
            raise ValidationError('At least input 1 option ffs.')


class MakePollForm(FlaskForm):
    name = StringField('Poll name:', validators=[DataRequired()])
    expiration = DateField('Expiration date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Create Poll')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError('Wrong username or password.')


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