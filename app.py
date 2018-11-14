from flask import Flask, render_template
from flask_mysqldb import MySQL
from forms import SQLForm, StatisticsForm
import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zMUVtqorW01Zke6F46w3U9M5QXZ6KCYY'
app.config['MYSQL_HOST'] = 'gamma.meteoadriatic.net'
app.config['MYSQL_USER'] = 'meteoadriatic-remote'
app.config['MYSQL_PASSWORD'] = 'Power/Off'
app.config['MYSQL_DB'] = 'reanalysis_test'
app.config['MYSQL_PORT'] = 33333
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
    # Initialize variables, form and mysql connection
    sql_response = ''
    sel_param = ''
    sel_loc = ''
    stats = ''
    table_truncated = False
    show_plot=False
    form = StatisticsForm()
    cur = mysql.connection.cursor()

    # Retrieve locations and populate select field
    cur.execute('''
        SELECT * FROM locations;
    ''')
    locations = cur.fetchall()
    locations = [i[0] for i in locations]
    form.locations.choices = locations

    # Retrieve parameters and populate select field
    cur.execute('''
        SELECT COLUMN_NAME  
        FROM information_schema.COLUMNS  
        WHERE TABLE_SCHEMA='reanalysis_test'    
        AND TABLE_NAME='model_output'    
        AND IS_NULLABLE='YES';
    ''')
    parameters = cur.fetchall()
    parameters = [i[0] for i in parameters]
    form.parameters.choices = parameters


    if form.is_submitted():
        # Retrieve user choice of location and parameter from select forms
        sel_loc = form.locations.data
        sel_param = form.parameters.data
        sel_startdate = form.startdate.data
        sel_enddate = form.enddate.data

        # Retrieve data from MySQL
        SQL = '''   SELECT datetime, {}
                    FROM model_output
                    WHERE location=%s
                    AND datetime > %s
                    AND datetime <= %s
                    ORDER BY datetime
            '''.format(sel_param)
        cur.execute(SQL, (sel_loc, sel_startdate, sel_enddate))
        sql_response = cur.fetchall()

        # Load MySQL response into pandas dataframe
        df = pd.DataFrame(list(sql_response))
        df = df.set_index([0])
        df.index.name = ''
        df.columns = [sel_param]

        # Build statistics list from df.describe() output
        statskeys=df.describe().index.tolist()
        statsvalues=df.describe().values.tolist()
        statsvalues = [item for sublist in statsvalues for item in sublist]
        statsvalues = ['%.1f' % elem for elem in statsvalues]
        stats = [list(a) for a in zip(statskeys, statsvalues)]

        # Create a plot from datetime (x axis) and chosen parameter (y axis)
        fig, ax = plt.subplots()
        fig.set_size_inches(12.5, 5.0)
        fig.tight_layout()
        fig.autofmt_xdate()
        ax.set_axisbelow(True)
        ax.grid(linestyle='--', linewidth='0.5', color='#41B3C5', alpha=0.8, axis='y')
        ax.plot(df.index, df[sel_param])

        # Save plot into file and set html trigger variable to display it
        fig.savefig('static/images/plot.png', bbox_inches = 'tight')
        show_plot=True

        # Limit number of table rows if user requested large amount of data
        if len(sql_response) > 720:
            sql_response = sql_response[:720]
            table_truncated = True


    return render_template('statistics.html',
                           title='Statistika',
                           form=form,
                           locations=locations,
                           parameters=parameters,
                           response=sql_response,
                           table_columns=['Datum i sat', sel_param],
                           stats=stats,
                           sel_param=sel_param,
                           sel_loc=sel_loc,
                           plot='/static/images/plot.png',
                           show_plot=show_plot,
                           table_truncated=table_truncated)


# Request browser not to cache responses (we need this for plots and other variable static content to work reliably)
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)