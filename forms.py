from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask import request

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    locations = SelectField('locations', choices=[], default='')
    parameters = SelectField('parameters', choices=[], default='')
    submit = SubmitField('Pošalji')

