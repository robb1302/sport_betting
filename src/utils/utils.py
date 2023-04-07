import config as CONFIG
import os
import pickle

def add_missing_dummy_columns( d, columns ):
    missing_cols = set( columns ) - set( d.columns )
    for c in missing_cols:
        d[c] = 0
    return d

def save_calc_pickle(calc, name):
    saved_pickle_path = CONFIG.SETTINGS_FOLDER
    filename = saved_pickle_path+name+'.sav'
    pickle.dump(calc, open(filename, 'wb'))

def load_calc_pickle(name):
    saved_pickle_path = CONFIG.SETTINGS_FOLDER
    calc = pickle.load(open(saved_pickle_path+name+'.sav', 'rb'))
    return calc

def createDirs(liga:list, data_path:str):
    # main_path = "C:/Users/Robert/Documents/Projekte/dev/bettingTool/data/leagues/" + liga
    # main_path = CONFIG.DATA_FOLDER+"/leagues/" + liga
    newpathMarktwert = f"{data_path}/{liga}/marktwert"
    newpathSeason = f"{data_path}/{liga}/season"
    newpathxG = f"{data_path}/{liga}/xg"
    newpathLineup = f"{data_path}/{liga}/lineup"
    
    directories = [newpathMarktwert, newpathSeason, newpathxG, newpathLineup]
    
    for d in directories:
        try:
            os.makedirs(d)
        except OSError:
            print ("Creation of the directory %s failed" % liga)

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

