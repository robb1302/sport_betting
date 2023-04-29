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

import pickle

def save_as_pickle(obj, target_path):
    # Save object as pickle file to target path
    with open(target_path, 'wb') as target_file:
        pickle.dump(obj, target_file)


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
            print ("Creation of the directory %s failed" % d)

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

import os

def get_dir_structure(root_dir):
    """
    Recursively gets the entire directory structure of a project.
    Returns a list of tuples, where the first element is the path to the directory,
    and the second element is a list of the names of the files in that directory.
    """
    dir_structure = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dir_structure.append((dirpath, filenames))
    return dir_structure

def create_dirs(dir_structure):
    """
    Creates all necessary directories based on the directory structure returned by get_dir_structure.
    """
    for dirpath, filenames in dir_structure:
        for dirname in dirpath.split(os.sep):
            if not os.path.exists(dirname):
                os.makedirs(dirname)
