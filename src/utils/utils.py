import config as CONFIG
import os
import pickle

def add_missing_dummy_columns(d, columns):
    missing_cols = set(columns) - set(d.columns)
    for c in missing_cols:
        d[c] = 0
    return d

def save_as_pickle(obj, target_path):
    # Save object as pickle file to target path
    with open(target_path, 'wb') as target_file:
        pickle.dump(obj, target_file)

def load_from_pickle(source_path):
    # Load object from pickle file
    with open(source_path, 'rb') as source_file:
        obj = pickle.load(source_file)
    return obj

def save_calc_pickle(calc, name):
    saved_pickle_path = CONFIG.SETTINGS_FOLDER
    filename = saved_pickle_path + name + '.sav'
    save_as_pickle(calc, filename)

def load_calc_pickle(name):
    saved_pickle_path = CONFIG.SETTINGS_FOLDER
    filename = saved_pickle_path + name + '.sav'
    return load_from_pickle(filename)

def createDirs(data_path, liga, *directories):
    """
    Creates the given directories in the specified data path and league directory.
    """
    for directory in directories:
        newpath = os.path.join(data_path, liga, directory)
        try:
            os.makedirs(newpath)
        except OSError:
            print(f"Creation of the directory {newpath} failed")

def boolean_string(s):
    return s.lower() == 'true'

def get_dir_structure(root_dir):
    """
    Recursively gets the entire directory structure of a project.
    Returns a list of tuples, where the first element is the path to the directory,
    and the second element is a list of the names of the files in that directory.
    """
    return [(dirpath, filenames) for dirpath, _, filenames in os.walk(root_dir)]
