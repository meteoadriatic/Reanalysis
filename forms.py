from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField, IntegerField, RadioField
from datetime import datetime
from wtforms.validators import InputRequired

class SQLForm(FlaskForm):
    sql = StringField('SQL')
    submit = SubmitField('Pošalji')

class StatisticsForm(FlaskForm):
    locations = SelectField('locations')
    locations2 = SelectField('locations2')
    locations3 = SelectField('locations3')
    locations4 = SelectField('locations4')
    locations5 = SelectField('locations5')
    parameters = SelectField('parameters')
    parameters2 = SelectField('parameters2')
    parameters3 = SelectField('parameters3')
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime(2018, 9, 1, 00, 00, 00, 00), validators=[InputRequired()])
    enddate = DateField('enddate', format='%Y-%m-%d', default=datetime(2018, 9, 30, 00, 00, 00, 00), validators=[InputRequired()])
    trendline = BooleanField('trendline')
    removetbllimit = BooleanField('removetbllimit')
    largeplot = BooleanField('largeplot')
    distribution = BooleanField('distribution')
    samey = BooleanField('samey')
    rollcorr = BooleanField('rollcorr')
    cumsum = BooleanField('cumsum')
    decompose = BooleanField('decompose')
    relativeplot = BooleanField('relativeplot')
    relativekde = BooleanField('relativekde')
    disablestats = BooleanField('disablestats')
    rollingwindow = IntegerField('rollingwindow', default=24, validators=[InputRequired()])
    rollingmean = BooleanField('rollingmean')
    rollingsum = BooleanField('rollingsum')
    rollingstdev = BooleanField('rollingstdev')
    fftspacing = IntegerField('fftspacing', default=0, validators=[InputRequired()])
    fftxmax = IntegerField('fftxmax', default=12, validators=[InputRequired()])
    ymaxplot = StringField('ymaxplot', default='0', validators=[InputRequired()])
    yminplot = StringField('yminplot', default='0', validators=[InputRequired()])
    elevation3d = StringField('elevation3d', default='45', validators=[InputRequired()])
    azimuth3d = StringField('azimuth3d', default='45', validators=[InputRequired()])
    limit3d = BooleanField('limit3d')
    plot3dbar = BooleanField('plot3dbar')
    min3d = StringField('min3d', default='0', validators=[InputRequired()])
    max3d = StringField('max3d', default='0', validators=[InputRequired()])
    resampleperiod = SelectField(choices=[('Off','Satni'),('D','Dnevni'),('M','Mjesečni'),('Y','Godišnji')],
                                 default='D')
    resamplehow = SelectField(choices=[('min', 'Minimum'), ('max', 'Maksimum'), ('mean', 'Srednjak'), ('sum', 'Suma')],
                              default='mean')
    submit = SubmitField('Pošalji')