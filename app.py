from config import *
from flask import render_template
from flask_mysqldb import MySQL
from forms import StatisticsForm
import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.dates import HourLocator, DayLocator, MonthLocator, YearLocator
import numpy as np
import params
import io
import base64

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', title='CRD Početna')

@app.route('/locations')
def locations():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT * FROM locations;
    ''')
    response = cur.fetchall()
    return render_template('locations.html',
                           title='Lokacije',
                           locs=response)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    # Initialize variables, form and mysql connection
    sql_response = ''
    sel_param = ''
    sel_param2 = ''
    sel_param_bak = ''
    sel_param2_bak = ''
    sel_loc = ''
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

    max_pri='N/A'
    min_pri='N/A'
    mean_pri='N/A'
    max_sec='N/A'
    min_sec='N/A'
    mean_sec='N/A'
    std_pri='N/A'
    std_sec='N/A'
    gmean_pri='N/A'
    hmean_pri='N/A'
    gmean_sec='N/A'
    hmean_sec='N/A'
    variation_pri='N/A'
    variation_sec='N/A'
    sum_pri='N/A'
    sum_sec='N/A'
    kurtosis_pri='N/A'
    kurtosis_sec='N/A'
    skew_pri='N/A'
    skew_sec='N/A'
    count_pri='N/A'
    count_sec='N/A'
    median_pri='N/A'
    median_sec='N/A'
    var_pri='N/A'
    var_sec='N/A'
    corr_pearson='N/A'
    corr_kendall='N/A'
    corr_spearman='N/A'
    slope_pri='N/A'
    intercept_pri='N/A' 
    r_value_pri='N/A'
    p_value_pri='N/A'
    std_err_pri='N/A'
    slope_sec='N/A'
    intercept_sec='N/A' 
    r_value_sec='N/A'
    p_value_sec='N/A'
    std_err_sec='N/A'

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
               'vtgrad_850_500',
               'thickness_1000_500',
               'thickness_1000_850',
               'thickness_850_500',
               'snow']
    parameters = parameters + appends
    parametersUF = parameters

    # Map user-friendly parameter names to parameters
    paramsUFmap = {'vtgrad_850_500': 'Vert. grad. temp. 850/500hPa',
                   'wdir_10': 'Smjer vjetra 10m',
                   'shear_10_850': 'Smicanje vjetra 10m/850hPa',
                   'wspd_500': 'Brzina vjetra 500hPa',
                   'HGT_0C': 'Visina 0°C nad tlom',
                   'wdir_300': 'Smjer vjetra 300hPa',
                   'wspd_850': 'Brzina vjetra 850hPa',
                   'precave': 'Satna količina oborine',
                   'rdrmax': 'Maks. radarska reflektivnost',
                   'VVEL_900': 'Vertikalno strujanje 900hPa',
                   'SNOD_SF': 'Visina snježnog pokrivača',
                   'wdir_500': 'Smjer vjetra 500hPa',
                   'UGRD_10': 'U komponenta vjetra 10m',
                   'VVEL_700': 'Vertikalno strujanje 700hPa',
                   'DLWRF_SF': 'Dolazno dugovalno zračenje',
                   'wdir_850': 'Smjer vjetra 850hPa',
                   'wspd_300': 'Brzina vjetra 300hPa',
                   'RH_700': 'Relativna vlažnost 700hPa',
                   'GUST_SF': 'Brzina udara vjetra',
                   'DSWRF_SF': 'Dolazno kratkovalno zračenje',
                   'UGRD_300': 'U komponenta vjetra 300hPa',
                   'TMP_1000': 'Temperatura 1000hPa',
                   'TMP_SF': 'Temperatura površine tla',
                   'HGT_500': 'Visina 500hPa',
                   'HGT_1000': 'Visina 1000hPa',
                   'shear_850_500': 'Smicanje vjetra 850/500hPa',
                   'TMP_850': 'Temperatura 850hPa',
                   'RH_2': 'Relativna vlažnost 2m',
                   'UGRD_850': 'U komponenta vjetra 850hPa',
                   'VGRD_500': 'V komponenta vjetra 500hPa',
                   'TMP_2': 'Temperatura 2m',
                   'CIN_180': 'Konvektivna inhibicija mixed layer',
                   'precpct': 'Vjerojatnost pojave satne oborine',
                   'HGT_850': 'Visina 850hPa',
                   'MSLET_SF': 'Tlak zraka reduciran na 0m',
                   'ULWRF_SF': 'Odlazno dugovalno zračenje',
                   'DPT_2': 'Temperatura rosišta 2m',
                   'VGRD_850': 'V komponenta vjetra 850hPa',
                   'PWAT_CLM': 'Oboriva voda',
                   'VGRD_300': 'V komponenta vjetra 300hPa',
                   'vtgrad_1000_850': 'Vert. grad. temp. 1000/850hPa',
                   'wspd_10': 'Brzina vjetra 10m',
                   'VGRD_10': 'V komponenta vjetra 10m',
                   'cldave': 'Postotak ukupne naoblake',
                   'shear_10_500': 'Smicanje vjetra 10m/500hPa',
                   'UGRD_500': 'U komponenta vjetra 500hPa',
                   'USWRF_SF': 'Odlazno kratkovalno zračenje',
                   'CAPE_180': 'Konv. pot. ener. mixed layer',
                   'TMP_500': 'Temperatura 500hPa',
                   'thickness_1000_500': 'Rel. topografija 1000/500hPa',
                   'thickness_1000_850': 'Rel. topografija 1000/850hPa',
                   'thickness_850_500': 'Rel. topografija 850/500hPa',
                   'snow': 'Satna količina snijega'}

    for x in parametersUF:
        if x in paramsUFmap:
            parametersUF = [i.replace(x, paramsUFmap.get(x)) for i in parametersUF]

    form.parameters.choices = parametersUF
    form.parameters2.choices = parametersUF

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
        rollingsum = int(form.rollingsum.data)
        cumsum = form.cumsum.data
        disablestats = form.disablestats.data
        rollcorr = int(form.rollcorr.data)
        fftspacing = int(form.fftspacing.data)
        fftxmax = int(form.fftxmax.data)
        ymaxplot = int(form.ymaxplot.data)
        yminplot = int(form.yminplot.data)

        # Define optimal xticks relative to requested time range
        def myxticks(sel_startdate, sel_enddate):
            timespan = (sel_enddate - sel_startdate).days
            plt.xlim(sel_startdate, sel_enddate)
            if timespan < 5:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d    '))
                ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
                ax.xaxis.set_major_locator(DayLocator())
                ax.xaxis.set_minor_locator(HourLocator(interval=6))
            elif timespan < 20:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(DayLocator())
            elif timespan < 50:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(DayLocator(interval=2))
            elif timespan < 180:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m   '))
                ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
                ax.xaxis.set_major_locator(MonthLocator())
                ax.xaxis.set_minor_locator(DayLocator(interval=4))
            elif timespan < 700:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                ax.xaxis.set_major_locator(MonthLocator())
            elif timespan < 2000:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y     '))
                ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
                ax.xaxis.set_major_locator(YearLocator())
                ax.xaxis.set_minor_locator(MonthLocator(interval=2))
            elif timespan < 10000:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                ax.xaxis.set_major_locator(YearLocator())
            else:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                ax.xaxis.set_major_locator(ticker.AutoLocator())

        sel_param_bak = sel_param
        sel_param2_bak = sel_param2

        if sel_param in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param:
                    sel_param = key

        if sel_param2 in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param2:
                    sel_param2 = key

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

            # Erroneous data cleanup
            if sel_param == 'precave':
                df.clip(lower=0, upper=None, inplace=True)

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

            # Erroneous data cleanup
            if sel_param == 'precave':
                df2.clip(lower=0, upper=None, inplace=True)

        '''
        Old statistics based on pandas df.describe(), not used anymore:
        
        # Build statistics list from df.describe() output
        statskeys = df.describe().index.tolist()
        statsvalues = df.describe().values.tolist()
        statsvalues = [item for sublist in statsvalues for item in sublist]
        statsvalues = ['%.1f' % elem for elem in statsvalues]
        stats = [list(a) for a in zip(statskeys, statsvalues)]
        '''

        if disablestats == False:
            # Perform detailed statistics on dataset
            from stats import variation, gmean, hmean, kurtosis, skew
            from scipy.stats import linregress

            max_pri = df[sel_param].max()
            min_pri = df[sel_param].min()
            if min_pri > 0:
                gmean_pri = gmean(df[sel_param].tolist()).round(1)
                hmean_pri = hmean(df[sel_param].tolist()).round(1)
            mean_pri = df[sel_param].mean().round(1)
            sum_pri = df[sel_param].sum().round(1)
            std_pri = df[sel_param].std().round(2)
            variation_pri = variation(df[sel_param].tolist()).round(3)
            kurtosis_pri = round(kurtosis(df[sel_param].tolist()), 3)
            skew_pri = round(skew(df[sel_param].tolist()), 3)
            median_pri = df[sel_param].median().round(1)
            count_pri = df[sel_param].count()
            var_pri =  df[sel_param].var().round(2)

            x = mdates.date2num(df.index)
            y = df[sel_param]
            slope_pri, intercept_pri, r_value_pri, p_value_pri, std_err_pri = linregress(x, y)
            slope_pri=round(slope_pri, 6)
            std_err_pri=round(std_err_pri, 5)

            if sel_param2 in parameters:
                max_sec = df2[sel_param2].max()
                min_sec = df2[sel_param2].min()
                if min_sec > 0:
                    gmean_sec = gmean(df2[sel_param2].tolist()).round(1)
                    hmean_sec = hmean(df2[sel_param2].tolist()).round(1)
                mean_sec = df2[sel_param2].mean().round(1)
                sum_sec = df2[sel_param2].sum().round(1)
                std_sec = df2[sel_param2].std().round(2)
                variation_sec = variation(df2[sel_param2].tolist()).round(3)
                kurtosis_sec = round(kurtosis(df2[sel_param2].tolist()), 3)
                skew_sec = round(skew(df2[sel_param2].tolist()), 3)
                median_sec = df2[sel_param2].median().round(1)
                count_sec = df2[sel_param2].count()
                var_sec = df2[sel_param2].var().round(2)

                x = mdates.date2num(df2.index)
                y = df2[sel_param2]
                slope_sec, intercept_sec, r_value_sec, p_value_sec, std_err_sec = linregress(x, y)
                slope_sec=round(slope_sec, 6)
                std_err_sec = round(std_err_sec, 5)

                corr_pearson = df[sel_param].corr(df2[sel_param2], method='pearson').round(3)
                corr_kendall = df[sel_param].corr(df2[sel_param2], method='kendall').round(3)
                corr_spearman = df[sel_param].corr(df2[sel_param2], method='spearman').round(3)


        # Apply rolling sum to plot data if requested by user
        if rollingsum != 0:
            df[sel_param] = df[sel_param].rolling(rollingsum).sum()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingsum).sum()
                df2.dropna(inplace=True)
        else:
            pass

        # Apply rolling mean to plot data if requested by user
        if rollingmean != 0:
            df[sel_param] = df[sel_param].rolling(rollingmean).mean()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingmean).mean()
                df2.dropna(inplace=True)
        else:
            pass

        # Apply cumulative sum to plot data if requested by user
        if cumsum == True:
            df[sel_param] = df[sel_param].cumsum()
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].cumsum()
        else:
            pass

        # Create a plot from datetime (x axis) and selected parameter (y axis)
        fig, ax = plt.subplots()
        if largeplot == True:
            fig.set_size_inches(12.5, 10.0)
        else:
            fig.set_size_inches(12.5, 5.0)
        fig.tight_layout()
        fig.autofmt_xdate(rotation=50, ha='center', which='both')
        ax.set_axisbelow(True)
        ax.grid(linestyle='--', linewidth='0.4', color='#E95420', alpha=0.5, axis='both')
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

        timespan=(sel_enddate-sel_startdate).days
        bigdata = 180
        # Customize plot according to selected parameter
        if sel_param == 'precave' or sel_param == 'precpct':
            if timespan < bigdata:
                ax.bar(df.index, df[sel_param], alpha=0.3, width=0.2, color='#772953')
            else:
                ax.plot(df.index, df[sel_param], color='#772953')
            ax.set_ylim(bottom=0)
        elif sel_param == 'snow':
            if timespan < bigdata:
                ax.bar(df.index, df[sel_param], alpha=0.3, color='#DC6EDC', width=0.2)
            else:
                ax.plot(df.index, df[sel_param], color='#DC6EDC')
            ax.set_ylim(bottom=0)
        elif sel_param == 'rdrmax':
            if timespan < bigdata:
                ax.bar(df.index, df[sel_param], alpha=0.3, color='#E95420', width=0.2)
            else:
                ax.plot(df.index, df[sel_param], color='#E95420')
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
            ax.plot(df.index, df[sel_param], color='#828282', alpha=0.31)
            ax.fill_between(df.index, 0, df[sel_param], color='#828282', alpha=0.3)
            ax.set_ylim(bottom=0)
        elif 'CAPE' in sel_param or 'shear' in sel_param:
            ax.plot(df.index, df[sel_param], color='#E95420')
            ax.fill_between(df.index, 0, df[sel_param], color='#E95420', alpha=0.3)
            ax.set_ylim(bottom=0)
        elif 'CIN' in sel_param:
            ax.plot(df.index, df[sel_param], color='#828282')
            ax.fill_between(df.index, df[sel_param], 0, color='#828282', alpha=0.3)
            ax.set_ylim(top=0)
        elif 'vtgrad' in sel_param:
            ax.plot(df.index, df[sel_param], color='#77216F')
            ax.fill_between(df.index, df[sel_param], 0, color='#77216F', alpha=0.13)
            ax.set_ylim(bottom=-0.01)
        else:
            ax.plot(df.index, df[sel_param], color='#77216F')

        # Plot secondary parameter
        if sel_param2 in parameters:
            if samey:
                ax.plot(df.index, df2[sel_param2], color='#111111', linewidth=0.28)
            else:
                ax2 = ax.twinx()
                ax2.plot(df.index, df2[sel_param2], color='#111111', linewidth=0.28)

        # Include linear trendline
        if trendline:
            x = mdates.date2num(df.index)
            y = df[sel_param]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            y_mean = [np.mean(df[sel_param])] * len(df.index)
            ax.plot(df.index, p(x), color='#2C001E')
            ax.plot(df.index, y_mean, linestyle='--', color='#AEA79F')
            plt.title("MEAN=%.3f TREND SLOPE=%.6fx" % (y_mean[0], z[0]))

        myxticks(sel_startdate, sel_enddate)

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
            from matplotlib.ticker import EngFormatter
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
            ax1.set_axisbelow(True)
            plt.title('FFT analiza frekvencije')
            formatter1 = EngFormatter(places=1, sep="\N{THIN SPACE}")
            ax1.yaxis.set_major_formatter(formatter1)
            ax1.plot(fftfreq[i], y_psd[i], color='#5E2750')
            ax1.fill_between(fftfreq[i], 0, y_psd[i], color='#77216F', alpha=0.3)
            plt.xlim(0, fftxmax)
            plt.ylim(bottom=0)

            y_fft_bis = y_fft.copy()
            y_fft_bis[np.abs(fftfreq) > 1] = 0
            y_slow = np.real(sp.fftpack.ifft(y_fft_bis))
            df[sel_param].plot(ax=ax, lw=1)
            ax4 = ax1.twinx().twiny()
            ax4.plot_date(df.index, y_slow, '-', color='#AEA79F', lw='1')
            ax4.set_axisbelow(True)
            ax4.grid(linestyle='--', linewidth='0.4', color='#E95420', alpha=0.5, axis='both')
            plt.xlim(sel_startdate, sel_enddate)
            plt.margins(x=0.0, y=0.3)
            ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax4.xaxis.set_major_locator(ticker.AutoLocator())

            # Save additional plot for FFT frequency spectrum
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            fft_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig1)

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
        if (sel_param2 in parameters) and (rollcorr == True) :
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
            fig3.autofmt_xdate(rotation=50, ha='center', which='both')
            ax3.set_axisbelow(True)
            ax3.grid(linestyle='--', linewidth='0.4', color='#41B3C5', alpha=0.5, axis='both')
            ax3.hlines(y=0, xmin=sel_startdate, xmax=sel_enddate, linewidth=1, color='black')
            ax3.set_ylim(top=1)
            ax3.set_ylim(bottom=-1)
            ax3.fill_between(df.index, 0, df['rollcorr'], color='#000000', alpha=1)
            plt.title('Pomična korelacija')

            plt.plot(df.index, df['rollcorr'], color='#000000', linewidth=1, alpha=1)

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

    # Join sql response tuples for primary and secondary parameter into one
    if sel_param2 in parameters:
        response = tuple(x + y for x, y in zip(sql_response, sql_response2))
    else:
        response = sql_response

    return render_template('statistics.html',
                           title='Statistika',
                           form=form,
                           locations=locations,
                           parameters=parametersUF,
                           first_date=first_date,
                           last_date=last_date,
                           response=response,
                           table_columns=['Datum i sat', sel_param_bak, sel_param2_bak],
                           sel_param=sel_param_bak,
                           sel_param2=sel_param2_bak,
                           sel_loc=sel_loc,
                           trendline=trendline,
                           removetbllimit=removetbllimit,
                           plot=plot_url,
                           fft=fft_url,
                           dist=dist_url,
                           rollcorr=rollcorr_url,
                           show_plot=show_plot,
                           table_truncated=table_truncated,
                           max_pri=max_pri,
                           min_pri=min_pri,
                           mean_pri=mean_pri,
                           max_sec=max_sec,
                           min_sec=min_sec,
                           mean_sec=mean_sec,
                           std_pri=std_pri,
                           std_sec=std_sec,
                           gmean_pri=gmean_pri,
                           gmean_sec=gmean_sec,
                           hmean_pri=hmean_pri,
                           hmean_sec=hmean_sec,
                           variation_pri=variation_pri,
                           variation_sec=variation_sec,
                           sum_pri=sum_pri,
                           sum_sec=sum_sec,
                           kurtosis_pri=kurtosis_pri,
                           kurtosis_sec=kurtosis_sec,
                           skew_pri=skew_pri,
                           skew_sec=skew_sec,
                           count_pri=count_pri,
                           count_sec=count_sec,
                           median_pri=median_pri,
                           median_sec=median_sec,
                           var_pri=var_pri,
                           var_sec=var_sec,
                           corr_pearson=corr_pearson,
                           corr_kendall=corr_kendall,
                           corr_spearman=corr_spearman,
                           slope_pri=slope_pri,
                           slope_sec=slope_sec,
                           std_err_pri=std_err_pri,
                           std_err_sec=std_err_sec)


@app.route('/map')
def map():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT latitude, longitude, name FROM locations;
    ''')
    response = cur.fetchall()
    return render_template('map.html',
                           title='Karta',
                           locs=response)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html',
                           title='Dokumentacija')

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