from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired


class Question(Form):
    options = SelectField(label=u'Pregunta?', coerce=int)

class Survey(FlaskForm):
    select_entries = FieldList(FormField(Question))
    submit = SubmitField('Responder')