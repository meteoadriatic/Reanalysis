from flask import Flask, render_template
from flask_mysqldb import MySQL
from forms import SQLForm, StatisticsForm
import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import params
import io
import base64

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
    sel_param2 = ''
    sel_loc = ''
    stats = ''
    trendline = False
    removetbllimit = False
    samey = False
    distribution = False
    table_truncated = False
    plot_url = ''
    fft_url = ''
    dist_url = ''
    rollcorr_url = ''
    show_plot = False
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

    # Append calculated parameters (params.py)
    appends = ['wspd_10', 'wdir_10',
               'wspd_850', 'wdir_850',
               'wspd_500', 'wdir_500',
               'wspd_300', 'wdir_300',
               'shear_10_500',
               'shear_850_500',
               'shear_10_850',
               'vtgrad_1000_850',
               'vtgrad_850_500']
    parameters = parameters + appends

    form.parameters.choices = parameters
    form.parameters2.choices = parameters

    # Retrieve first and last datetime from database
    cur.execute('''
        SELECT datetime FROM model_output ORDER BY datetime LIMIT 1;
    ''')
    first_date = cur.fetchall()
    cur.execute('''
        SELECT datetime FROM model_output ORDER BY datetime DESC LIMIT 1;
    ''')
    last_date = cur.fetchall()



    if form.is_submitted():
        # Retrieve user choice of location and parameter from select forms
        sel_loc = form.locations.data
        sel_param = form.parameters.data
        sel_param2 = form.parameters2.data
        sel_startdate = form.startdate.data
        sel_enddate = form.enddate.data
        trendline = form.trendline.data
        removetbllimit = form.removetbllimit.data
        largeplot = form.largeplot.data
        distribution = form.distribution.data
        samey = form.samey.data
        rollingmean = int(form.rollingmean.data)
        fftspacing = int(form.fftspacing.data)
        ymaxplot = int(form.ymaxplot.data)
        yminplot = int(form.yminplot.data)

        # Primary parameter processing
        # Separate functions for parameters derived from raw sql data
        paramsfunc = getattr(params, sel_param, None)
        if sel_param in appends:
            df = paramsfunc(cur, sel_loc, sel_startdate, sel_enddate)
            sql_response = tuple(zip(df.index, df[sel_param]))
        else:
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
            df.set_index([0], inplace=True)
            df.index.name = ''
            df.columns = [sel_param]

        if sel_param2 in parameters:
            # Secondary parameter processing
            # Separate functions for parameters derived from raw sql data
            paramsfunc = getattr(params, sel_param2, None)
            if sel_param2 in appends:
                df2 = paramsfunc(cur, sel_loc, sel_startdate, sel_enddate)
                sql_response2 = tuple(zip(df2.index, df2[sel_param2]))
            else:
            # Retrieve data from MySQL
                SQL2 = '''  SELECT datetime, {}
                            FROM model_output
                            WHERE location=%s
                            AND datetime > %s
                            AND datetime <= %s
                            ORDER BY datetime
                    '''.format(sel_param2)
                cur.execute(SQL2, (sel_loc, sel_startdate, sel_enddate))
                sql_response2 = cur.fetchall()

                # Load MySQL response into pandas dataframe
                df2 = pd.DataFrame(list(sql_response2))
                df2.set_index([0], inplace=True)
                df2.index.name = ''
                df2.columns = [sel_param2]

        # Build statistics list from df.describe() output
        statskeys = df.describe().index.tolist()
        statsvalues = df.describe().values.tolist()
        statsvalues = [item for sublist in statsvalues for item in sublist]
        statsvalues = ['%.1f' % elem for elem in statsvalues]
        stats = [list(a) for a in zip(statskeys, statsvalues)]

        # Apply rolling mean to plot data if requested by user
        if rollingmean != 0:
            df[sel_param] = df[sel_param].rolling(rollingmean).mean()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingmean).mean()
                df2.dropna(inplace=True)
        else:
            pass

        # Create a plot from datetime (x axis) and selected parameter (y axis)
        fig, ax = plt.subplots()
        if largeplot == True:
            fig.set_size_inches(12.5, 10.0)
        else:
            fig.set_size_inches(12.5, 5.0)
        fig.tight_layout()
        fig.autofmt_xdate()
        ax.set_axisbelow(True)
        ax.grid(linestyle='--', linewidth='0.4', color='#41B3C5', alpha=0.5, axis='both')
        if sel_param2 in parameters:
            plt.title(str(sel_param) + ', ' + str(sel_param2))
        else:
            plt.title(sel_param)

        if ymaxplot != 0:
            ax.set_ylim(top=ymaxplot)
        else:
            pass
        if yminplot != 0:
            ax.set_ylim(bottom=yminplot)
        else:
            pass

        # Customize plot according to selected parameter
        if sel_param == 'precave' or sel_param == 'precpct':
            ax.bar(df.index, df[sel_param], alpha=0.15)
            ax.set_ylim(bottom=0)
        elif sel_param == 'rdrmax':
            ax.bar(df.index, df[sel_param], alpha=0.3, color='red', width=0.2)
            ax.set_ylim(bottom=0)
        elif 'wdir_' in sel_param or 'VVEL' in sel_param:
            scatsiz=max((100000/(len(df.index))),50)
            ax.scatter(df.index, df[sel_param], s=scatsiz, alpha=0.1)
        elif 'SWRF' in sel_param or 'LWRF' in sel_param\
                or 'RH_' in sel_param or 'PWAT' in sel_param:
            ax.plot(df.index, df[sel_param])
            ax.fill_between(df.index, 0, df[sel_param], color='#41B3C5', alpha=0.3)
            ax.set_ylim(bottom=0)
        elif 'cldave' in sel_param:
            ax.plot(df.index, df[sel_param], color='#828282')
            ax.fill_between(df.index, 0, df[sel_param], color='#828282', alpha=0.3)
            ax.set_ylim(bottom=0)
        elif 'CAPE' in sel_param or 'shear' in sel_param:
            ax.plot(df.index, df[sel_param], color='red')
            ax.fill_between(df.index, 0, df[sel_param], color='#FF9600', alpha=0.3)
            ax.set_ylim(bottom=0)
        elif 'CIN' in sel_param:
            ax.plot(df.index, df[sel_param], color='#828282')
            ax.fill_between(df.index, df[sel_param], 0, color='#828282', alpha=0.3)
            ax.set_ylim(top=0)
        elif 'vtgrad' in sel_param:
            ax.plot(df.index, df[sel_param], color='#1A74B1')
            ax.fill_between(df.index, df[sel_param], 0, color='#1A74B1', alpha=0.13)
            ax.set_ylim(bottom=-0.01)
        else:
            ax.plot(df.index, df[sel_param], color='#1A74B1')

        # Plot secondary parameter
        if sel_param2 in parameters:
            if samey:
                ax.plot(df.index, df2[sel_param2], color='#000000', linewidth=0.3)
            else:
                ax2 = ax.twinx()
                ax2.plot(df.index, df2[sel_param2], color='#000000', linewidth=0.3)

        # Include linear trendline
        if trendline:
            x = mdates.date2num(df.index)
            y = df[sel_param]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            y_mean = [np.mean(df[sel_param])] * len(df.index)
            ax.plot(df.index, p(x), color='black')
            ax.plot(df.index, y_mean, linestyle='--', color='teal')
            plt.title("MEAN=%.3f TREND SLOPE=%.6fx" % (y_mean[0], z[0]))

        # Make x-axis ticks evenly spaced - auto spacing doesn't look nice on matplotib v3
        plt.xlim(sel_startdate, sel_enddate)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(ticker.AutoLocator())

        # Save plot into memory
        img = io.BytesIO()
        plt.savefig(img, bbox_inches = 'tight', format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)
        show_plot=True

        # FFT
        if fftspacing != 0:
            import scipy as sp
            import scipy.fftpack
            y_fft = sp.fftpack.fft(df[sel_param])
            y_psd = np.abs(y_fft) ** 2
            fftfreq = sp.fftpack.fftfreq(len(y_psd), 1 / fftspacing)
            i = fftfreq > 0

            # Initialize separate plot for FF frequency spectrum
            fig1, ax1 = plt.subplots(sharex=False, sharey=False, clear=True)
            if largeplot == True:
                fig1.set_size_inches(12.5, 6.0)
            else:
                fig1.set_size_inches(12.5, 3.0)
            fig1.tight_layout()
            plt.title('FFT analiza frekvencije')
            ax1.plot(fftfreq[i], y_psd[i])

            # Save additional plot for FFT frequency spectrum
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            fft_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig1)

            y_fft_bis = y_fft.copy()
            y_fft_bis[np.abs(fftfreq) > 1] = 0
            y_slow = np.real(sp.fftpack.ifft(y_fft_bis))
            df[sel_param].plot(ax=ax, lw=0.5)
            ax.plot_date(df.index, y_slow, '-', color='green', lw='3')
            ax.set_axisbelow(True)
            ax.grid(linestyle='--', linewidth='0.4', color='#41B3C5', alpha=0.5, axis='both')
        else:
            pass

        # Distribution histogram
        if distribution:
            fig2, ax2 = plt.subplots(sharex=False, sharey=False, clear=True)
            if largeplot == True:
                fig2.set_size_inches(12.5, 6.0)
            else:
                fig2.set_size_inches(12.5, 3.0)
            fig2.tight_layout()
            plt.title('Distribucija')

            plt.hist(x=df[sel_param], color='#E88B0C', alpha=0.7, rwidth=0.9, bins=20)

            # Save additional plot for distribution histogram
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            dist_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig2)
        else:
            pass

        # Rolling correlation plot
        if sel_param2 in parameters:
            if rollingmean==0:
                window=3
            else:
                window=rollingmean
            df['rollcorr'] = df[sel_param].rolling(window).corr(df2[sel_param2])
            fig3, ax3 = plt.subplots(sharex=False, sharey=False, clear=True)
            if largeplot == True:
                fig3.set_size_inches(12.5, 6.0)
            else:
                fig3.set_size_inches(12.5, 3.0)
            fig3.tight_layout()
            fig3.autofmt_xdate()
            ax3.set_axisbelow(True)
            ax3.grid(linestyle='--', linewidth='0.4', color='#41B3C5', alpha=0.5, axis='both')
            ax3.hlines(y=0, xmin=sel_startdate, xmax=sel_enddate, linewidth=1, color='black')
            ax3.set_ylim(top=1)
            ax3.set_ylim(bottom=-1)
            ax3.fill_between(df.index, 0, df['rollcorr'], color='#000000', alpha=0.4)
            plt.title('Pomična korelacija')

            plt.plot(df.index, df['rollcorr'], color='#FF8B00', linewidth=3)

            plt.xlim(sel_startdate, sel_enddate)
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax3.xaxis.set_major_locator(ticker.AutoLocator())

            # Save additional plot for distribution histogram
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            rollcorr_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig3)
        else:
            pass


        # Limit number of table rows if user requested large amount of data
        if removetbllimit == False:
            if len(sql_response) > 720:
                sql_response = sql_response[:720]
                table_truncated = True
        else:
            pass


    return render_template('statistics.html',
                           title='Statistika',
                           form=form,
                           locations=locations,
                           parameters=parameters,
                           first_date=first_date,
                           last_date=last_date,
                           response=sql_response,
                           table_columns=['Datum i sat', sel_param],
                           stats=stats,
                           sel_param=sel_param,
                           sel_param2=sel_param2,
                           sel_loc=sel_loc,
                           trendline=trendline,
                           removetbllimit=removetbllimit,
                           plot=plot_url,
                           fft=fft_url,
                           dist=dist_url,
                           rollcorr=rollcorr_url,
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