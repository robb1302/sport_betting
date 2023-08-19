import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace('scripts','')
sys.path.append(parent_dir)

from src.utils.utils import load_from_pickle
import config as CONFIG

import numpy as np
import pandas as pd
print('Start')
df = load_from_pickle(CONFIG.DATA_FOLDER_RAW+'main_leagues_database_raw.sav')
df['Date'] = pd.to_datetime(df['Date'])
# convert the day, month, and year columns to datetime format
df = df.reset_index()

from src.utils.utils import load_from_pickle
df = load_from_pickle(source_path= CONFIG.DATA_FOLDER_RAW+'main_leagues_database_raw.sav')
df = df[~df.FTR.isna()]

bet_attributes = ['IWH','IWD','IWA','BWH','BWD','BWA','B365H','B365D','B365A']
df['Date'] = pd.to_datetime(df['Date'])
complete_bets =  df[bet_attributes].isna().T.sum()==0
df = df[complete_bets] 

X = df[["HomeTeam","AwayTeam","Div","B365H","B365D","B365A","BWH","BWD","BWA","IWH","IWD","IWA"]]
X.head()

y = df[["B365H","B365D","B365A","FTR"]]

y.columns =["H","D","A","R"]

import pandas as pd

def make_y(y_row):
    r = y_row["R"]
    y_row[r] = y_row[r]-1
    results = {'H','D','A'}
    y_row[list(results - {r})] = 0
    return y_row

# apply the make_y function to every row of the DataFrame
y= y.apply(lambda x: make_y(x), axis=1)
df = pd.concat([X,y],axis=1)
df.to_csv(CONFIG.DATA_FOLDER_PROCESSED+'model_data.csv')
