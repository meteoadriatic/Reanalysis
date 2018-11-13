from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
from forms import SQLForm, StatisticsForm
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zMUVtqorW01Zke6F46w3U9M5QXZ6KCYY'
app.config['MYSQL_HOST'] = 'gamma.meteoadriatic.net'
app.config['MYSQL_USER'] = 'meteoadriatic-remote'
app.config['MYSQL_PASSWORD'] = 'Power/Off'
app.config['MYSQL_DB'] = 'reanalysis_test'
app.config['MYSQL_PORT'] = 33333

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', title='CRD - Climate Reanalysis Database')

@app.route('/locations')
def locations():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT * FROM locations;
    ''')
    response = cur.fetchall()
    return render_template('locations.html',
                           title='CRD - Climate Reanalysis Database',
                           locs=response)

@app.route('/sql', methods=['GET', 'POST'])
def sql():
    form = SQLForm()
    sql_response = None

    if form.is_submitted():
        sql_query = form.sql.data
        cur = mysql.connection.cursor()
        cur.execute(sql_query)
        sql_response = cur.fetchall()

    return render_template('sql.html',
                           title='SQL upit',
                           form=form,
                           response=sql_response)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    form = StatisticsForm()
    sql_response = ''
    sel_param = ''
    sel_loc = ''
    stats = ''
    cur = mysql.connection.cursor()

    cur.execute('''
        SELECT * FROM locations;
    ''')
    locations = cur.fetchall()
    locations = [i[0] for i in locations]

    cur.execute('''
        SELECT COLUMN_NAME  
        FROM information_schema.COLUMNS  
        WHERE TABLE_SCHEMA='reanalysis_test'    
        AND TABLE_NAME='model_output'    
        AND IS_NULLABLE='YES';
    ''')
    parameters = cur.fetchall()
    parameters = [i[0] for i in parameters]

    form.locations.choices = locations
    form.parameters.choices = parameters

    if form.is_submitted():
        sel_loc = form.locations.data
        sel_param = form.parameters.data
        sel_startdate = form.startdate.data
        sel_enddate = form.enddate.data

        SQL = '''   SELECT datetime, {}
                    FROM model_output
                    WHERE location=%s
                    AND datetime > %s
                    AND datetime <= %s
            '''.format(sel_param)

        cur.execute(SQL, (sel_loc, sel_startdate, sel_enddate))
        sql_response = cur.fetchall()

        df = pd.DataFrame(list(sql_response))
        df = df.set_index([0])
        df.columns = [sel_param]

        statsvalues=df.describe().values.tolist()
        statskeys=df.describe().index.tolist()
        stats = [list(a) for a in zip(statskeys, statsvalues)]


    return render_template('statistics.html',
                           title='Statistika',
                           form=form,
                           locations=locations,
                           parameters=parameters,
                           response=sql_response,
                           table_columns=['Datum i sat', sel_param],
                           stats=stats,
                           sel_param=sel_param,
                           sel_loc=sel_loc)




if __name__ == '__main__':
    app.run(debug=True)