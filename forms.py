from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask import request

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    location = SelectField('location', choices=[])
    parameter = SelectField('parameter', choices=[])
    submit = SubmitField('Pošalji')

