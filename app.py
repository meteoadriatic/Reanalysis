from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

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
    #return str(rv)

    return render_template('index.html',
                           title='CRD - Climate Reanalysis Database',
                           mydata=str(rv))





if __name__ == '__main__':
    app.run(debug=True)