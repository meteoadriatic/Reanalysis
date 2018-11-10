from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask import request

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    location = SelectField('locations', coerce=str)
    parameter = SelectField('parameters', coerce=str)
    submit = SubmitField('Pošalji')

