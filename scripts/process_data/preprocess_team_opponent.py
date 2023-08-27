# DELETE

def find_and_append_module_path():
    import sys
    import os
    current_directory = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_directory.find(substring_to_find)
    
    if index != -1:
        parent_dir = os.path.join(current_directory[:index], substring_to_find)
        sys.path.append(parent_dir)
find_and_append_module_path()
from src.utils.utils import createDirs
import config as CONFIG


from src.features import load_team_opponent
from src.features.preprocess import derived_odds,get_bookmaker, get_odd_pred_team_opponent, split_date,add_last_3_scores_column
import numpy as np
import pandas as pd

# Import preprocessing functions
from src.features.preprocess import (
    derived_odds, get_bookmaker, get_odd_pred_team_opponent,
    split_date, add_last_3_scores_column
)

# Import necessary configurations
import config as CONFIG

def preprocess_data(df):

    standard_attributes = ['Target', 'atHome', 'Date', 'Div']
    # Your preprocessing steps here

    df = split_date(df)
    df = df.sort_values(['year', 'month', 'day'], ascending=False)
    df = df.reset_index()

  
    bookmaker_attributes = get_bookmaker(bm='BW', df=df) + get_bookmaker(bm='B365', df=df) + get_bookmaker(bm='IW', df=df)
    bet_on_team = get_bookmaker(bm='Team', df=df[bookmaker_attributes])
    bet_on_opponent = get_bookmaker(bm='Opponent', df=df[bookmaker_attributes])
    bet_on_draw = get_bookmaker(bm='Draw', df=df[bookmaker_attributes])

    df_derived_b365 = get_odd_pred_team_opponent(bet="B365", df=df)
    df_derived_iw = get_odd_pred_team_opponent(bet="IW", df=df)
    df_derived_bw = get_odd_pred_team_opponent(bet="BW", df=df)

    df_derived_team = derived_odds(sight='Team', df=df, odds=bet_on_team)
    df_derived_opponent = derived_odds(sight='Opponent', df=df, odds=bet_on_opponent)
    df_derived_draw = derived_odds(sight='Draw', df=df, odds=bet_on_draw)

    df["diff_FTG_against_Opponent"] = df["FTG_Team"] - df["FTG_Opponent"]
    df["diff_ShotsOnTarget_against_Opponent"] = df["ShotsOnTarget_Team"] - df["ShotsOnTarget_Opponent"]

    df = add_last_3_scores_column(df=df, score_column="diff_FTG_against_Opponent", anz_games=4)
    df = add_last_3_scores_column(df=df, score_column="diff_ShotsOnTarget_against_Opponent", anz_games=4)
    df = add_last_3_scores_column(df=df, score_column="B365_Team", anz_games=4)
    df = add_last_3_scores_column(df=df, score_column="B365_Opponent", anz_games=4)

    rolling_mean_attributes = [c for c in df.columns if 'last' in c]

    if ('FTG_Team' in df.columns) & ('FTG_Opponent' in df.columns):
        df['Target'] = df.FTG_Team > df.FTG_Opponent
        df['Target'].value_counts()
        standard_attributes=+['Target']
    df = df.dropna()


    model_data = pd.concat([df[rolling_mean_attributes], df[standard_attributes], df[bookmaker_attributes],
                            df[["Team", "month", "year"]], df_derived_team, df_derived_opponent, df_derived_draw,
                            df_derived_b365, df_derived_iw, df_derived_bw], axis=1)

    model_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    model_data = model_data.Date[~model_data.Date.isna()]

    return model_data

# Example usage:
if __name__ == "__main__":
    # Load your data into df here
    df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
    
    processed_data = preprocess_data(df)
    processed_data.to_csv(CONFIG.DATA_FOLDER_PROCESSED + 'model_data_all.csv')
    print('Done')
