from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from flask import request
from datetime import datetime

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    locations = SelectField('locations', choices=[], default='')
    parameters = SelectField('parameters', choices=[], default='')
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime(2018, 9, 1, 00, 00, 00, 00))
    enddate = DateField('enddate', format='%Y-%m-%d', default=datetime(2018, 9, 30, 00, 00, 00, 00))
    submit = SubmitField('Pošalji')

