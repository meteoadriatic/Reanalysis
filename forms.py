from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField, IntegerField
from datetime import datetime
from wtforms.validators import InputRequired

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    locations = SelectField('locations', default='Zadar')
    parameters = SelectField('parameters')
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime(2018, 9, 1, 00, 00, 00, 00), validators=[InputRequired()])
    enddate = DateField('enddate', format='%Y-%m-%d', default=datetime(2018, 9, 30, 00, 00, 00, 00), validators=[InputRequired()])
    trendline = BooleanField('trendline')
    removetbllimit = BooleanField('removetbllimit')
    largeplot = BooleanField('largeplot')
    rollingmean = IntegerField('rollingmean', default=0, validators=[InputRequired()])
    fftspacing = IntegerField('fftspacing', default=0, validators=[InputRequired()])
    ymaxplot = StringField('ymaxplot', default='0', validators=[InputRequired()])
    yminplot = StringField('yminplot', default='0', validators=[InputRequired()])
    submit = SubmitField('Pošalji')