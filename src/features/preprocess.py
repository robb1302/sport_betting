import pickle
import pandas as pd
import config as CONFIG
import numpy as np 

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

def get_bookmaker(bm:str,df):
    return [i for i in df.columns if bm in i]

def derived_odds(sight:str,df:pd.DataFrame,odds:list):
    return_df = pd.DataFrame()
    return_df[f'Max_{sight}'] = df[odds].apply(max,axis=1)
    return_df[f'Min_{sight}'] = df[odds].apply(min,axis=1)
    return_df[f'Avg_{sight}'] = df[odds].apply(np.average,axis=1)

    return_df[f'Span_{sight}'] = return_df[f'Max_{sight}']-return_df[f'Min_{sight}'] 
    return_df[f'Ratio_{sight}'] = return_df[f'Max_{sight}']/return_df[f'Min_{sight}'] 
    return return_df

def set_dummies_div(df, cat, divs=[]):
    if cat in df.columns:
        if divs == []:
            divs = list(set(df[cat]))
        for d in divs:
            df[d] = [1 if ele == d else 0 for ele in df[cat]]
        df = df.drop(cat, axis=1)
    return df

def get_odd_pred(bet,df):
    odd_team = df[bet+"_Team"]
    odd_opponent = df[bet+"_Opponent"]
    odd_draw = df[bet+"_Draw"]
    sum_odds = odd_team + odd_opponent + odd_draw
    odd_pred = pd.DataFrame(index=df.index)
    odd_pred[bet+"_Team_odd_pred"]=odd_team/sum_odds
    odd_pred[bet+"_opponent_odd_pred"]=odd_opponent/sum_odds
    odd_pred[bet+"_Team_draw_pred"]=odd_draw/sum_odds
    
    return odd_pred