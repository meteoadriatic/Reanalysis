from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')
