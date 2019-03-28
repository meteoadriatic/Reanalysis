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
import seaborn as sns
sns.set_style("white")

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
    cur = mysql.connection.cursor()
    form = StatisticsForm()

    # Set variables' defaults
    sql_response = sel_param = sel_param2 = sel_param3 = sel_param_bak = sel_param2_bak = sel_param3_bak = sel_loc = ''
    min3d =  max3d = plot_url = fft_url = dist_url = relplot_url = rollcorr_url = plot3d_url = ''
    trendline = removetbllimit = samey = distribution = table_truncated = limit3d = plot3dbar = show_plot = False
    max_pri = min_pri = mean_pri = max_sec = min_sec = mean_sec = std_pri = std_sec = gmean_pri = hmean_pri = 'N/A'
    gmean_sec = hmean_sec = variation_pri = variation_sec = sum_pri = sum_sec = kurtosis_pri = kurtosis_sec = 'N/A'
    skew_pri = skew_sec = count_pri = count_sec = median_pri = median_sec = var_pri = var_sec = corr_pearson = 'N/A'
    corr_kendall = corr_spearman = slope_pri = intercept_pri = r_value_pri = p_value_pri = std_err_pri = 'N/A'
    slope_sec = intercept_sec = r_value_sec = p_value_sec = std_err_sec = 'N/A'

    # Retrieve locations and populate select field
    from functions import retrieve_locations
    locations = retrieve_locations(cur=cur)
    form.locations.choices = locations

    # Retrieve parameters and populate select field
    from functions import retrieve_parameters
    parameters = retrieve_parameters(cur)

    # Append calculated parameters (params.py)
    from functions import append_calculates
    parameters, appends = append_calculates(parameters)
    parametersUF = parameters

    # Map user-friendly parameter names to parameters
    from functions import user_friendly_paramnames
    paramsUFmap = user_friendly_paramnames()
    for x in parametersUF:
        if x in paramsUFmap:
            parametersUF = [i.replace(x, paramsUFmap.get(x)) for i in parametersUF]
    form.parameters.choices = parametersUF
    form.parameters2.choices = parametersUF
    form.parameters3.choices = parametersUF

    # Retrieve first and last datetime from database
    from functions import first_available_date, last_available_date
    first_date = first_available_date(cur)
    last_date = last_available_date(cur)

    if form.is_submitted():
        # Retrieve user choice of location and parameter from select forms
        sel_loc = form.locations.data
        sel_param = form.parameters.data
        sel_param2 = form.parameters2.data
        sel_param3 = form.parameters3.data
        sel_startdate = form.startdate.data
        sel_enddate = form.enddate.data
        trendline = form.trendline.data
        removetbllimit = form.removetbllimit.data
        largeplot = form.largeplot.data
        distribution = form.distribution.data
        samey = form.samey.data
        scatter_plot = form.scatterplot.data
        scatter_alpha = float(form.scatteralpha.data)
        scatter_size = float(form.scattersize.data)
        rollingwindow = int(form.rollingwindow.data)
        rollingmean = form.rollingmean.data
        rollingsum = form.rollingsum.data
        rollingstdev = form.rollingstdev.data
        cumsum = form.cumsum.data
        decompose = form.decompose.data
        relativeplot = form.relativeplot.data
        relativekde = form.relativekde.data
        disablestats = form.disablestats.data
        rollcorr = int(form.rollcorr.data)
        fftspacing = int(form.fftspacing.data)
        fftxmax = int(form.fftxmax.data)
        ymaxplot = float(form.ymaxplot.data)
        yminplot = float(form.yminplot.data)
        limit3d = form.limit3d.data
        plot3dbar = form.plot3dbar.data
        min3d = float(form.min3d.data)
        max3d = float(form.max3d.data)
        elevation3d = int(form.elevation3d.data)
        azimuth3d = int(form.azimuth3d.data)
        resampleperiod = form.resampleperiod.data
        resamplehow = form.resamplehow.data
        sql_filter = form.sqlfilter.data
        filter_pri_min = form.filterprimin.data
        filter_pri_max = form.filterprimax.data

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
        sel_param3_bak = sel_param3

        if sel_param in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param:
                    sel_param = key

        if sel_param2 in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param2:
                    sel_param2 = key

        if sel_param3 in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param3:
                    sel_param3 = key

        # Primary parameter processing
        # Functions for additional parameters derived from raw sql data in params.py
        paramsfunc = getattr(params, sel_param, None)
        if sel_param in appends:
            df = paramsfunc(cur, sel_loc, sel_startdate, sel_enddate, sql_filter)
            sql_response = tuple(zip(df.index, df[sel_param]))
        else:
        # Retrieve data from MySQL
            SQL = '''   SELECT datetime, {}
                        FROM model_output
                        WHERE location=%s
                        AND datetime > %s
                        AND datetime <= %s
                        {}
                        ORDER BY datetime
                '''.format(sel_param, sql_filter)
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
                sql_response = tuple(zip(df.index, df[sel_param]))

        # Resample data if requested
        if resampleperiod != 'Off':
            df = df.groupby(pd.Grouper(freq=resampleperiod))[sel_param].agg([resamplehow]).round(1)
            df.columns = [sel_param]
            sql_response = tuple(zip(df.index, df[sel_param]))

        # Filter data by min/max values if requested
        if filter_pri_min:
            filter_pri_min = float(filter_pri_min)
            df = df[df[sel_param] >= filter_pri_min]
        if filter_pri_max:
            filter_pri_max = float(filter_pri_max)
            df = df[df[sel_param] <= filter_pri_max]

        if sel_param2 in parameters:
            # Secondary parameter processing
            # Functions for additional parameters derived from raw sql data in params.py
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
                if sel_param2 == 'precave':
                    df2.clip(lower=0, upper=None, inplace=True)
                    sql_response2 = tuple(zip(df2.index, df2[sel_param2]))

            # Resample data if requested
            if resampleperiod != 'Off':
                df2 = df2.groupby(pd.Grouper(freq=resampleperiod))[sel_param2].agg([resamplehow]).round(1)
                df2.columns = [sel_param2]
                sql_response2 = tuple(zip(df2.index, df2[sel_param2]))
                

        if sel_param3 in parameters:
            # 3D parameter processing
            # Functions for additional parameters derived from raw sql data in params.py
            paramsfunc = getattr(params, sel_param3, None)
            if sel_param3 in appends:
                df3 = paramsfunc(cur, sel_loc, sel_startdate, sel_enddate)
            else:
            # Retrieve data from MySQL
                SQL3 = '''  SELECT datetime, {}
                            FROM model_output
                            WHERE location=%s
                            AND datetime > %s
                            AND datetime <= %s
                            ORDER BY datetime
                    '''.format(sel_param3)
                cur.execute(SQL3, (sel_loc, sel_startdate, sel_enddate))
                sql_response3 = cur.fetchall()

                # Load MySQL response into pandas dataframe
                df3 = pd.DataFrame(list(sql_response3))
                df3.set_index([0], inplace=True)
                df3.index.name = ''
                df3.columns = [sel_param3]

                # Erroneous data cleanup
                if sel_param3 == 'precave':
                    df3.clip(lower=0, upper=None, inplace=True)

            # Resample data if requested
            if resampleperiod != 'Off':
                df3 = df3.groupby(pd.Grouper(freq=resampleperiod))[sel_param3].agg([resamplehow]).round(1)
                df3.columns = [sel_param3]




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
        if rollingsum == True:
            df[sel_param] = df[sel_param].rolling(rollingwindow).sum()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingwindow).sum()
                df2.dropna(inplace=True)
        else:
            pass

        # Apply rolling mean to plot data if requested by user
        if rollingmean == True:
            df[sel_param] = df[sel_param].rolling(rollingwindow).mean()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingwindow).mean()
                df2.dropna(inplace=True)
        else:
            pass

        # Apply rolling standard deviation to plot data if requested by user
        if rollingstdev == True:
            df[sel_param] = df[sel_param].rolling(rollingwindow).std()
            df.dropna(inplace=True)
            if sel_param2 in parameters:
                df2[sel_param2] = df2[sel_param2].rolling(rollingwindow).std()
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

        df_rows = df.shape[0]
        #timespan=(sel_enddate-sel_startdate).days
        bigdata = 150
        if resampleperiod == 'M':
            barwidthfactor=28
        elif resampleperiod == 'Y':
            barwidthfactor=330
        else:
            barwidthfactor=0.9
        # Customize plot according to selected parameter
        if sql_filter or scatter_plot or\
                filter_pri_min or filter_pri_max\
                or filter_pri_min == 0 or filter_pri_max == 0:
            ax.plot(df.index, df[sel_param], '.', color='#77216F', alpha=scatter_alpha, markersize=scatter_size)
        else:
            if sel_param == 'precave' or sel_param == 'precpct':
                if df_rows < bigdata:
                    ax.bar(df.index, df[sel_param], alpha=0.7, color='#772953', width=barwidthfactor)
                else:
                    ax.plot(df.index, df[sel_param], color='#772953')
                ax.set_ylim(bottom=0)
            elif sel_param == 'snow':
                if df_rows < bigdata:
                    ax.bar(df.index, df[sel_param], alpha=0.7, color='#DC6EDC', width=barwidthfactor)
                else:
                    ax.plot(df.index, df[sel_param], color='#DC6EDC')
                ax.set_ylim(bottom=0)
            elif sel_param == 'rdrmax':
                if df_rows < bigdata:
                    ax.scatter(df.index, df[sel_param], alpha=0.9, color='#E95420')
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

        if ymaxplot != 0:
            ax.set_ylim(top=ymaxplot)
        else:
            pass
        if yminplot != 0:
            ax.set_ylim(bottom=yminplot)
        else:
            pass

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




        # 3D plot
        if (sel_param2 in parameters) and (sel_param3 in parameters):
            # This import registers the 3D projection, but is otherwise unused.
            from mpl_toolkits import mplot3d
            import matplotlib.cm as cmx
            from matplotlib import rcParams
            if largeplot == True:
                rcParams['figure.figsize'] = 12.5, 10.0
            else:
                rcParams['figure.figsize'] = 12.5, 6.0

            cm = plt.get_cmap('jet')
            cNorm = matplotlib.colors.Normalize(vmin=min(df3[sel_param3]), vmax=max(df3[sel_param3]))
            scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

            fig_3d = plt.figure()
            ax_3d = plt.axes(projection='3d')
            ax_3d.view_init(elevation3d, azimuth3d)

            fig_3d.tight_layout()
            ax_3d.set_axisbelow(True)
            plt.title('3D graf zavisnosti trećeg parametra o primarnom i sekundarnom parametru')

            if limit3d == True:
                df3.mask((df3 < min3d) | (df3 > max3d), inplace=True)

            if plot3dbar == False:
                ax_3d.scatter(df[sel_param], df2[sel_param2], df3[sel_param3],
                            c=scalarMap.to_rgba(df3[sel_param3]))
            else:
                dataset_length = df[sel_param].size
                datarange_sel_param = df[sel_param].max() - df[sel_param].min()
                datarange_sel_param2 = df2[sel_param2].max() - df2[sel_param2].min()
                datarange_sel_param3 = df3[sel_param3].max() - df3[sel_param3].min()
                #dx = (datarange_sel_param / 35) * np.ones(dataset_length) * (df3[sel_param3]/datarange_sel_param3)
                #dy = (datarange_sel_param2 / 35) * np.ones(dataset_length) * (df3[sel_param3]/datarange_sel_param3)
                dx = (datarange_sel_param / 60) * np.ones(dataset_length)
                dy = (datarange_sel_param2 / 60) * np.ones(dataset_length)
                ax_3d.bar3d(df[sel_param], df2[sel_param2], np.zeros(dataset_length), dx, dy, df3[sel_param3],
                            color=scalarMap.to_rgba(df3[sel_param3]))

            ax_3d.set_xlabel(sel_param)
            ax_3d.set_ylabel(sel_param2)
            ax_3d.set_zlabel(sel_param3)
            scalarMap.set_array(df3[sel_param3])
            if plot3dbar == False:
                fig_3d.colorbar(scalarMap, shrink=0.5, aspect=5)
            else:
                fig_3d.colorbar(scalarMap, shrink=0.5, aspect=15)

            # Save plot into memory
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            plot3d_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig_3d)


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


        # Relative plot
        if (sel_param2 in parameters) and (relativeplot == True):

            if relativekde == False:
                fig_rel, ax_rel = plt.subplots(sharex=False, sharey=False, clear=True)
                if largeplot == True:
                    fig_rel.set_size_inches(12.5, 10.0)
                else:
                    fig_rel.set_size_inches(12.5, 5.0)
                fig_rel.tight_layout()

                ax_rel.set_axisbelow(True)
                plt.title('Odnos primarnog i sekundarnog parametra')
                ax_rel.scatter(df[sel_param], df2[sel_param2], color='#E95420', alpha=0.4, s=100)
                plt.xlabel(sel_param)
                plt.ylabel(sel_param2)
                ax_rel.set_axisbelow(True)
                ax_rel.grid(linestyle='--', linewidth='0.4', color='#77216F', alpha=0.5, axis='both')
            else:
                sns.set_style("whitegrid", {'grid.linestyle': '--'})
                from matplotlib import rcParams
                if largeplot == True:
                    rcParams['figure.figsize'] = 12.5, 10.0
                else:
                    rcParams['figure.figsize'] = 12.5, 5.0
                x = df[sel_param]
                y = df2[sel_param2]
                cmap = sns.cubehelix_palette(light=1, as_cmap=True)
                kdeplot = sns.kdeplot(x, y,
                                      cmap=cmap,
                                      shade=True,
                                      shade_lowest=False).set_title('Odnos primarnog i sekundarnog parametra')
                fig_rel = kdeplot.get_figure()

            # Save plot into memory
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            relplot_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig_rel)


        # Seasonal decompose plot
        timespan = (sel_enddate - sel_startdate).days
        if decompose and (timespan > 730):
            dcmpsf=None
            import statsmodels.api as sm
            if resampleperiod == 'Off':
                dcmpsf = 8760
            if resampleperiod == 'D':
                dcmpsf = 365
            if resampleperiod == 'M':
                dcmpsf = 12
            if resampleperiod == 'Y':
                dcmpsf = 1
            print(dcmpsf)
            dcmps = sm.tsa.seasonal_decompose(df[sel_param], freq=dcmpsf)
            fig_dcmps = dcmps.plot()
            if largeplot == True:
                fig_dcmps.set_size_inches(12.5, 10.0)
            else:
                fig_dcmps.set_size_inches(12.5, 5.0)

            # Save plot into memory
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            relplot_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig_dcmps)

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
                           sel_param3=sel_param3_bak,
                           sel_loc=sel_loc,
                           trendline=trendline,
                           removetbllimit=removetbllimit,
                           plot=plot_url,
                           fft=fft_url,
                           dist=dist_url,
                           relplot=relplot_url,
                           plot3d=plot3d_url,
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


@app.route('/compare_locations', methods=['GET', 'POST'])
def compare_locations():
    cur = mysql.connection.cursor()
    form = StatisticsForm()

    # Set variables' defaults
    sql_response = sel_param = sel_param_bak = sel_loc = sel_loc2 = sel_loc3 = sel_loc4 = sel_loc5 = ''
    compareplot_url = ''
    show_plot = False

    # Retrieve locations and populate select field
    from functions import retrieve_locations
    locations = retrieve_locations(cur=cur)
    form.locations.choices = locations

    # Retrieve parameters and populate select field
    from functions import retrieve_parameters
    parameters = retrieve_parameters(cur)

    # Append calculated parameters (params.py)
    from functions import append_calculates
    parameters, appends = append_calculates(parameters)
    parametersUF = parameters

    # Map user-friendly parameter names to parameters
    from functions import user_friendly_paramnames
    paramsUFmap = user_friendly_paramnames()
    for x in parametersUF:
        if x in paramsUFmap:
            parametersUF = [i.replace(x, paramsUFmap.get(x)) for i in parametersUF]
    form.parameters.choices = parametersUF

    # Retrieve first and last datetime from database
    from functions import first_available_date, last_available_date
    first_date = first_available_date(cur)
    last_date = last_available_date(cur)

    if form.is_submitted():
        # Retrieve user choice of location and parameter from select forms
        sel_loc = form.locations.data
        sel_loc2 = form.locations2.data
        sel_loc3 = form.locations3.data
        sel_loc4 = form.locations4.data
        sel_loc5 = form.locations5.data
        sel_param = form.parameters.data
        sel_startdate = form.startdate.data
        sel_enddate = form.enddate.data

        sel_param_bak = sel_param

        if sel_param in paramsUFmap.values():
            for key, value in paramsUFmap.items():
                if value == sel_param:
                    sel_param = key

        if sel_loc in locations:
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
            df.columns = [sel_loc]

        if sel_loc2 in locations:
            # Retrieve data from MySQL
            SQL = '''   SELECT datetime, {}
                        FROM model_output
                        WHERE location=%s
                        AND datetime > %s
                        AND datetime <= %s
                        ORDER BY datetime
                '''.format(sel_param)
            cur.execute(SQL, (sel_loc2, sel_startdate, sel_enddate))
            sql_response = cur.fetchall()

            # Load MySQL response into pandas dataframe
            dfB = pd.DataFrame(list(sql_response))
            dfB.set_index([0], inplace=True)
            dfB.index.name = ''
            dfB.columns = [sel_loc2]
            df = pd.merge(df, dfB, left_index=True, right_index=True)

            if sel_loc3 in locations:
                # Retrieve data from MySQL
                SQL = '''   SELECT datetime, {}
                            FROM model_output
                            WHERE location=%s
                            AND datetime > %s
                            AND datetime <= %s
                            ORDER BY datetime
                    '''.format(sel_param)
                cur.execute(SQL, (sel_loc3, sel_startdate, sel_enddate))
                sql_response = cur.fetchall()

                # Load MySQL response into pandas dataframe
                dfB = pd.DataFrame(list(sql_response))
                dfB.set_index([0], inplace=True)
                dfB.index.name = ''
                dfB.columns = [sel_loc3]
                df = pd.merge(df, dfB, left_index=True, right_index=True)

            if sel_loc4 in locations:
                # Retrieve data from MySQL
                SQL = '''   SELECT datetime, {}
                            FROM model_output
                            WHERE location=%s
                            AND datetime > %s
                            AND datetime <= %s
                            ORDER BY datetime
                    '''.format(sel_param)
                cur.execute(SQL, (sel_loc4, sel_startdate, sel_enddate))
                sql_response = cur.fetchall()

                # Load MySQL response into pandas dataframe
                dfB = pd.DataFrame(list(sql_response))
                dfB.set_index([0], inplace=True)
                dfB.index.name = ''
                dfB.columns = [sel_loc4]
                df = pd.merge(df, dfB, left_index=True, right_index=True)

            if sel_loc5 in locations:
                # Retrieve data from MySQL
                SQL = '''   SELECT datetime, {}
                            FROM model_output
                            WHERE location=%s
                            AND datetime > %s
                            AND datetime <= %s
                            ORDER BY datetime
                    '''.format(sel_param)
                cur.execute(SQL, (sel_loc5, sel_startdate, sel_enddate))
                sql_response = cur.fetchall()

                # Load MySQL response into pandas dataframe
                dfB = pd.DataFrame(list(sql_response))
                dfB.set_index([0], inplace=True)
                dfB.index.name = ''
                dfB.columns = [sel_loc5]
                df = pd.merge(df, dfB, left_index=True, right_index=True)

            ax = df.plot(figsize=(12.5, 10), title='Grafička usporedba lokacija po odabranom parametru')
            fig = ax.get_figure()
            ax.set_ylabel(sel_param_bak)

            # Save plot into memory
            img = io.BytesIO()
            plt.savefig(img, bbox_inches='tight', format='png')
            img.seek(0)
            compareplot_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig)
            show_plot = True


    return render_template('compare_locations.html',
                           title='Usporedba lokacija',
                           form=form,
                           locations=locations,
                           parameters=parametersUF,
                           first_date=first_date,
                           last_date=last_date,
                           table_columns=['Datum i sat', sel_param_bak],
                           sel_param=sel_param_bak,
                           sel_loc=sel_loc,
                           sel_loc2=sel_loc2,
                           sel_loc3=sel_loc3,
                           sel_loc4=sel_loc4,
                           sel_loc5=sel_loc5,
                           compareplot=compareplot_url,
                           show_plot=show_plot
                           )


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