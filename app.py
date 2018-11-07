from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

'''
Note, after pulling on gamma:
1) Uncomment SERVER_NAME
2) Change MYSQL_HOST to 127.0.0.1
'''

#app.config['SERVER_NAME'] = 'gamma.meteoadriatic.net'
app.config['MYSQL_HOST'] = 'gamma.meteoadriatic.net'
app.config['MYSQL_USER'] = 'meteoadriatic-remote'
app.config['MYSQL_PASSWORD'] = 'Power/Off'
app.config['MYSQL_DB'] = 'reanalysis_test'
app.config['MYSQL_PORT'] = 33333

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT TMP_2, RH_2 FROM model_output WHERE location = 'zadar' AND datetime = '2018-09-01 01:00:00'
    ''')
    rv = cur.fetchall()

    return render_template('index.html',
                           title='CRD - Climate Reanalysis Database',
                           mydata=str(rv))

@app.route('/locations')
def locations():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT * FROM locations;'
    ''')
    response = cur.fetchall()
    return render_template('locations.html',
                           title='CRD - Climate Reanalysis Database',
                           locs=response)



if __name__ == '__main__':
    app.run(debug=True)