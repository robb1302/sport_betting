import pickle
import pandas as pd
import config as CONFIG

def load_team_opponent(filename_main:str):


    df = pickle.load(open(filename_main, 'rb'))
    mapping = pd.read_csv(CONFIG.DATA_FOLDER_MAPPING+'mapping_team_opponent.csv',",")


    map_home = dict()
    map_away=dict()
    for i in mapping.columns:
        if mapping[i][0]!="x":
            map_home[i] = mapping[i][0]
        if mapping[i][1]!="x":
            map_away[i] = mapping[i][1]

    df_home = df[[i for i in df.columns if i in  map_home]].rename(map_home,axis=1)
    df_home['atHome']=True
    #df_home.index = df_home.index+'__home' 
    df_away = df[[i for i in df.columns if i in  map_away]].rename(map_away,axis=1)
    df_away['atHome']=False
    #df_away.index = df_away.index+'__away' 

    df_team_opponent = pd.concat([df_home,df_away],axis=0)
    return df_team_opponent

def split_date(df):
    if 'Date' in df.columns:
        new_date = (df["Date"].str.split("/",expand=True))
        new_date.columns = ["day","month","year"]
        new_date = new_date.astype('int')

        new_date.year[new_date.year < 2000] = new_date.year[new_date.year < 2000]+2000

        df = pd.concat([df,new_date],axis=1)
    else:
        print('Keine Spalte "Date" in Spalten vorhanden')
    return df