from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
from forms import SQLForm, StatisticsForm

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

    form = StatisticsForm(locations)
    if form.is_submitted():
        print(form.location.data)
        print(form.parameter.data)

        '''
        Ovi printovi iznad su samo radi testa tu da vidim što mi vraća (ništa očito)
        Cilj ovoga je naravno da se ono što je odabrano u ova dva select-a proslijedi unutar
        sql upita u bazu... naravno fali tu još input-a (npr. nešto za odabrati range datuma)
        i onda sam planirao da mi vrati natrag statističke podatke za odabranu lokaciju (tmin, tmax, ....)
        Možda čak bez select-a za parametar da vrati svu statistiku za lokaciju koju definiram negdje u kodu.
        '''

    return render_template('statistics.html',
                           title='Statistika',
                           form=form,
                           locations=locations,
                           parameters=parameters)






if __name__ == '__main__':
    app.run(debug=True)