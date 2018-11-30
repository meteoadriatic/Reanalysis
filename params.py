import pandas as pd
import numpy as np

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
    df.loc[(df['wspd_10'].isnull()), 'wspd_10'] = ((df[1] ** 2 + df[2] ** 2) ** 0.5)
    df = df[['wspd_10']].astype(int)
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
    df.loc[(df['wdir_10'].isnull()), 'wdir_10'] = (57.3 * np.arctan2(df[1], df[2]) + 180)
    df = df[['wdir_10']].astype(int)
    df.index.name = ''

    return df

def wspd_850(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_850, VGRD_850
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
    df['wspd_850'] = np.nan
    df.loc[(df['wspd_850'].isnull()), 'wspd_850'] = ((df[1] ** 2 + df[2] ** 2) ** 0.5)
    df = df[['wspd_850']].astype(int)
    df.index.name = ''

    return df

def wdir_850(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_850, VGRD_850
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
    df['wdir_850'] = np.nan
    df.loc[(df['wdir_850'].isnull()), 'wdir_850'] = (57.3 * np.arctan2(df[1], df[2]) + 180)
    df = df[['wdir_850']].astype(int)
    df.index.name = ''

    return df

def wspd_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_500, VGRD_500
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
    df['wspd_500'] = np.nan
    df.loc[(df['wspd_500'].isnull()), 'wspd_500'] = ((df[1] ** 2 + df[2] ** 2) ** 0.5)
    df = df[['wspd_500']].astype(int)
    df.index.name = ''

    return df

def wdir_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_500, VGRD_500
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
    df['wdir_500'] = np.nan
    df.loc[(df['wdir_500'].isnull()), 'wdir_500'] = (57.3 * np.arctan2(df[1], df[2]) + 180)
    df = df[['wdir_500']].astype(int)
    df.index.name = ''

    return df

def wspd_300(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_300, VGRD_300
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
    df['wspd_300'] = np.nan
    df.loc[(df['wspd_300'].isnull()), 'wspd_300'] = ((df[1] ** 2 + df[2] ** 2) ** 0.5)
    df = df[['wspd_300']].astype(int)
    df.index.name = ''

    return df

def wdir_300(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_300, VGRD_300
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
    df['wdir_300'] = np.nan
    df.loc[(df['wdir_300'].isnull()), 'wdir_300'] = (57.3 * np.arctan2(df[1], df[2]) + 180)
    df = df[['wdir_300']].astype(int)
    df.index.name = ''

    return df

def shear_10_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_10, VGRD_10, UGRD_500, VGRD_500
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
    df['shear_10_500'] = np.nan
    df.loc[(df['shear_10_500'].isnull()), 'shear_10_500'] = \
        (np.sqrt(abs(df[3]-df[1]) ** 2 + (abs(df[4]-df[2])) ** 2))
    df = df[['shear_10_500']].astype(int)
    df.index.name = ''

    return df

def shear_850_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_850, VGRD_850, UGRD_500, VGRD_500
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
    df['shear_850_500'] = np.nan
    df.loc[(df['shear_850_500'].isnull()), 'shear_850_500'] = \
        (np.sqrt(abs(df[3]-df[1]) ** 2 + (abs(df[4]-df[2])) ** 2))
    df = df[['shear_850_500']].astype(int)
    df.index.name = ''

    return df

def shear_10_850(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, UGRD_10, VGRD_10, UGRD_850, VGRD_850
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
    df['shear_10_850'] = np.nan
    df.loc[(df['shear_10_850'].isnull()), 'shear_10_850'] = \
        (np.sqrt(abs(df[3]-df[1]) ** 2 + (abs(df[4]-df[2])) ** 2))
    df = df[['shear_10_850']].astype(int)
    df.index.name = ''

    return df

def vtgrad_1000_850(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, TMP_1000, TMP_850, HGT_1000, HGT_850
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
    df['vtgrad_1000_850'] = np.nan
    df.loc[(df['vtgrad_1000_850'].isnull()), 'vtgrad_1000_850'] = \
        (df[2]-df[1])/(df[4]-df[3]).round(4)
    df = df[['vtgrad_1000_850']]
    df.index.name = ''

    return df

def vtgrad_850_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, TMP_850, TMP_500, HGT_850, HGT_500
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
    df['vtgrad_850_500'] = np.nan
    df.loc[(df['vtgrad_850_500'].isnull()), 'vtgrad_850_500'] = \
        (df[2]-df[1])/(df[4]-df[3])
    df = df[['vtgrad_850_500']].round(4)
    df.index.name = ''

    return df

def thickness_1000_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, HGT_1000, HGT_500
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
    df['thickness_1000_500'] = np.nan
    df.loc[(df['thickness_1000_500'].isnull()), 'thickness_1000_500'] = df[2]-df[1]
    df = df[['thickness_1000_500']].astype(int)
    df.index.name = ''

    return df

def thickness_1000_850(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, HGT_1000, HGT_850
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
    df['thickness_1000_850'] = np.nan
    df.loc[(df['thickness_1000_850'].isnull()), 'thickness_1000_850'] = df[2]-df[1]
    df = df[['thickness_1000_850']].astype(int)
    df.index.name = ''

    return df

def thickness_850_500(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, HGT_850, HGT_500
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
    df['thickness_850_500'] = np.nan
    df.loc[(df['thickness_850_500'].isnull()), 'thickness_850_500'] = df[2]-df[1]
    df = df[['thickness_850_500']].astype(int)
    df.index.name = ''

    return df

def snow(cur, sel_loc, sel_startdate, sel_enddate):
    SQL = '''   SELECT datetime, precave, HGT_0C, TMP_2, RH_2, TMP_850
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
    df['snow'] = np.nan
    df.loc[(df['snow'].isnull()), 'snow'] = \
        np.clip(df[1] *  (1 - (np.clip(((np.clip(df[2],0,None)
                                + 200 * df[3]) /2
                                - np.clip(4 * (100 - df[4]), 0, None)
                                + np.clip((df[5] + 1) * 100, 0, None)),
                                0, None)) / 750), 0, 100)
    df = df[['snow']].round(1)
    df.index.name = ''

    return df
