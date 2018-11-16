import pandas as pd
import numpy as np

# from vulkan:
# df.loc[(df['wspd'].isnull()), 'wspd'] = (df['u10'] ** 2 + df['v10'] ** 2) ** 0.5
# df.loc[(df['wd'].isnull()), 'wd'] = 57.3 * np.arctan2(df['u10'], df['v10']) + 180

def wspd_10(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_10, VGRD_10
                FROM model_output
                WHERE location=%s
                AND datetime > %s
                AND datetime <= %s
                ORDER BY datetime
        '''
    cur.execute(SQL, (sel_loc, sel_startdate, sel_enddate))
    sql_response = cur.fetchall()

    df = pd.DataFrame(list(sql_response))
    df.set_index([0], inplace=True)
    df['wspd_10'] = np.nan
    df.loc[(df['wspd_10'].isnull()), 'wspd_10'] = ((df[1] ** 2 + df[2] ** 2) ** 0.5).astype(int)
    df = df[['wspd_10']]
    df.index.name = ''

    return df

def wdir_10(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_10, VGRD_10
                FROM model_output
                WHERE location=%s
                AND datetime > %s
                AND datetime <= %s
                ORDER BY datetime
        '''
    cur.execute(SQL, (sel_loc, sel_startdate, sel_enddate))
    sql_response = cur.fetchall()

    df = pd.DataFrame(list(sql_response))
    df.set_index([0], inplace=True)
    df['wdir_10'] = np.nan
    df.loc[(df['wdir_10'].isnull()), 'wdir_10'] = (57.3 * np.arctan2(df[1], df[2]) + 180).astype(int)
    df = df[['wdir_10']]
    df.index.name = ''

    return df