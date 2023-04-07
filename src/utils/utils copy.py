import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from builtins import len
from src.provideData.stats import readLeague
import os
import keras.backend as K
import src.utils.globals as GLOBALS
import json
import pickle

def add_missing_dummy_columns( d, columns ):
    missing_cols = set( columns ) - set( d.columns )
    for c in missing_cols:
        d[c] = 0
    return d

def fix_columns( d, columns ):  

    d  = add_missing_dummy_columns( d, columns )

    # make sure we have all the columns we need
    assert( set( columns ) - set( d.columns ) == set())

    extra_cols = set( d.columns ) - set( columns )
    if extra_cols:
        print ("extra columns:", extra_cols)

    d = d[ columns ]
    return d
def save_calc_pickle(calc, name):
    saved_pickle_path = GLOBALS.SETTINGS_FOLDER
    filename = saved_pickle_path+name+'.sav'
    pickle.dump(calc, open(filename, 'wb'))
def load_calc_pickle(name):
    saved_pickle_path = GLOBALS.SETTINGS_FOLDER
    calc = pickle.load(open(saved_pickle_path+name+'.sav', 'rb'))
    return calc

def save_settings(name,file):
    path_settings = GLOBALS.SETTINGS_FOLDER
    with open(path_settings+name+'.json', "w") as outfile: 
        json.dump(file, outfile)
def load_settings(name):
    path_settings = GLOBALS.SETTINGS_FOLDER
    with open(path_settings+name+'.json') as outfile: 
        output=json.load(outfile)
    return output
def which(self):
    try:
        self = list(iter(self))
    except TypeError as e:
        raise Exception("""'which' method can only be applied to iterables.
        {}""".format(str(e)))
    indices = [i for i, x in enumerate(self) if bool(x) == True]
    return(indices)


def createDirs(liga):
#    main_path = "C:/Users/Robert/Documents/Projekte/dev/bettingTool/data/leagues/" + liga
    main_path = GLOBALS.DATA_FOLDER+"/leagues/" + liga
    newpathMarktwert = main_path + "/marktwert"
    newpathSeason = main_path + "/season"
    newpathxG = main_path + "/xG"
    newpathLineup = main_path + "/lineup"
    
    createDirs = [newpathMarktwert, newpathSeason, newpathxG, newpathLineup]
    for path in createDirs:
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

def findWinner(value, PTS=True):
    # 1 or higher means the home team won
    if(PTS == True):
        if (value > 0):
            return(3)
        # 0 means a tie
        elif (value == 0):
            return(1)
    # Otherwise, the away team must have won
        else:
            return(0)
    else:
        if (value > 0):
            return("H")
         # 0 means a tie
        elif (value == 0):
            return("D")
    # Otherwise, the away team must have won
        else:
            return("A")


def corr_heatmap(data):
    corr_matrix = data.corr()
    mask = np.zeros_like(corr_matrix, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(11, 15)) 
    heatmap = sns.heatmap(corr_matrix,
                          mask=mask,
                          square=True,
                          linewidths=.5,
                          cmap='coolwarm',
                          cbar_kws={'shrink': .4,
                                    'ticks' : [-1, -.5, 0, 0.5, 1]},
                          vmin=-1,
                          vmax=1,
                          annot=True,
                          annot_kws={'size': 12})  # add the column names as labels
    ax.set_yticklabels(corr_matrix.columns, rotation=0)
    ax.set_xticklabels(corr_matrix.columns)
    sns.set_style({'xtick.bottom': True}, {'ytick.left': True})

    
def print_full(x):
    pd.set_option('display.max_columns', x.shape[1])
    print(x)
    pd.reset_option('display.max_rows')

    
def getTable(league="D1", season="1819"):
    # Lade entsprechende Liga
    df = readLeague(liga=league, season=season)
    choosenAttributes = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
    df = df[choosenAttributes]

    # erstelle Heimtabelle
    df['GD'] = df['FTHG'] - df['FTAG']
    df['PTS'] = df['GD'].apply(findWinner)
    homeTable = df.groupby("HomeTeam").sum()
    homeTable["Team"] = homeTable.index
    homeTable.columns = ["GF" , "GA" , "GD"  , "PTS", "Team"]
    
    # Auswaertstabelle
    df['GD'] = -df['FTHG'] + df['FTAG']
    df['PTS'] = df['GD'].apply(findWinner)
    awayTable = df.groupby("AwayTeam").sum()
    awayTable["Team"] = awayTable.index
    awayTable.columns = ["GA" , "GF" , "GD"  , "PTS", "Team"]
    
    totalTable = pd.concat([awayTable, homeTable])
    # gib die Gesamttabelle zurueck
    totalTable = totalTable.groupby("Team").sum().sort_values(by=['PTS'], ascending=False)
    totalTable["Team"] = totalTable.index
    return(totalTable)


def read_settings(data, path=GLOBALS.SETTINGS_FOLDER):
    # Liest JSON Datei mit Settings ein
    # Opening JSON file
    f = open(path + data + '.json',)

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return data


def get_f1(y_true, y_pred):  # taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2 * (precision * recall) / (precision + recall + K.epsilon())
    return f1_val

# This function take a dataframe
# as a parameter and returning list
# of column names whose contents 
# are duplicates.
def getDuplicateColumns(df):
  
    # Create an empty set
    duplicateColumnNames = set()
      
    # Iterate through all the columns 
    # of dataframe
    for x in range(df.shape[1]):
          
        # Take column at xth index.
        col = df.iloc[:, x]
          
        # Iterate through all the columns in
        # DataFrame from (x + 1)th index to
        # last index
        for y in range(x + 1, df.shape[1]):
              
            # Take column at yth index.
            otherCol = df.iloc[:, y]
              
            # Check if two columns at x & y
            # index are equal or not,
            # if equal then adding 
            # to the set
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[y])
                  
    # Return list of unique column names 
    # whose contents are duplicates.
    return list(duplicateColumnNames)
