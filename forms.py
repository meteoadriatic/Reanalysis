from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField
from datetime import datetime

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    locations = SelectField('locations', default='Zadar')
    parameters = SelectField('parameters')
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime(2018, 9, 1, 00, 00, 00, 00))
    enddate = DateField('enddate', format='%Y-%m-%d', default=datetime(2018, 9, 30, 00, 00, 00, 00))
    trendline = BooleanField('trendline')
    removetbllimit = BooleanField('removetbllimit')
    rollingmean = StringField('rollingmean', default='0')
    submit = SubmitField('Pošalji')