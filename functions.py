
def retrieve_locations(cur):
    # Retrieve locations
    cur.execute('''
        SELECT * FROM locations;
    ''')
    locations = cur.fetchall()
    locations = [i[0] for i in locations]
    return locations

def retrieve_parameters(cur):
    cur.execute('''
        SELECT COLUMN_NAME  
        FROM information_schema.COLUMNS  
        WHERE TABLE_SCHEMA='reanalysis_test'    
        AND TABLE_NAME='model_output'    
        AND IS_NULLABLE='YES';
    ''')
    parameters = cur.fetchall()
    parameters = [i[0] for i in parameters]
    return parameters

def append_calculates(parameters):
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
    return parameters, appends

def user_friendly_paramnames():
    paramsUFmap = {'vtgrad_850_500': 'Vert. grad. temp. 850/500hPa',
                   'wdir_10': 'Smjer vjetra 10m',
                   'shear_10_850': 'Smicanje vjetra 10m/850hPa',
                   'wspd_500': 'Brzina vjetra 500hPa',
                   'HGT_0C': 'Visina 0°C nad tlom',
                   'wdir_300': 'Smjer vjetra 300hPa',
                   'wspd_850': 'Brzina vjetra 850hPa',
                   'precave': 'Akumulirana količina oborine',
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
                   'snow': 'Akumulirana količina snijega'}
    return paramsUFmap

def first_available_date(cur):
    cur.execute('''
        SELECT datetime FROM model_output ORDER BY datetime LIMIT 1;
    ''')
    first_date = cur.fetchall()
    return first_date

def last_available_date(cur):
    cur.execute('''
        SELECT datetime FROM model_output ORDER BY datetime DESC LIMIT 1;
    ''')
    last_date = cur.fetchall()
    return last_date
