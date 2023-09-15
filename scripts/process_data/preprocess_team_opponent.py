import os
import sys
import pandas as pd
import numpy as np


def find_and_append_module_path():
    current_dir = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_dir.rfind(substring_to_find)
    
    if index != -1:
        # Extract the directory path up to and including the last "mypath" occurrence
        new_dir = current_dir[:index + (len(substring_to_find))]

        # Change the current working directory to the new directory
        os.chdir(new_dir)
        sys.path.append(new_dir)
        # Verify the new current directory
        print("New current directory:", os.getcwd())
    else:
        print("No 'mypath' found in the current directory")

def preprocess_data(df):
    print('start preprocessing')
    
    standard_attributes = ['atHome', 'Div']
    # Your preprocessing steps here

    df = split_date(df)
    df = df.sort_values(['year', 'month', 'day'], ascending=False)
    df = df.reset_index()

  
    bookmaker_attributes = get_bookmaker(bm='WH', df=df) + get_bookmaker(bm='IW', df=df) # + get_bookmaker(bm='B365', df=df) 
    bet_on_team = get_bookmaker(bm='Team', df=df[bookmaker_attributes])
    bet_on_opponent = get_bookmaker(bm='Opponent', df=df[bookmaker_attributes])
    bet_on_draw = get_bookmaker(bm='Draw', df=df[bookmaker_attributes])

    # df_derived_b365 = get_odd_pred_team_opponent(bet="B365", df=df)
    df_derived_iw = get_odd_pred_team_opponent(bet="IW", df=df)
    df_derived_bw = get_odd_pred_team_opponent(bet="BW", df=df)
    df_derived_wh = get_odd_pred_team_opponent(bet="WH", df=df)

    df_derived_team = derived_odds(sight='Team', df=df, odds=bet_on_team)
    df_derived_opponent = derived_odds(sight='Opponent', df=df, odds=bet_on_opponent)
    df_derived_draw = derived_odds(sight='Draw', df=df, odds=bet_on_draw)

    if len(df.FTG_Team!=df.FTG_Team.isna().sum()):
        df['Target'] = df.FTG_Team > df.FTG_Opponent
        df['Target'].value_counts()
        standard_attributes+=['Target']

    model_data = pd.concat([df[standard_attributes], df[bookmaker_attributes],
                            df[["Team","Opponent", "month", "year"]], df_derived_team, df_derived_opponent, df_derived_draw,
                             df_derived_iw, df_derived_wh], axis=1)

    model_data.replace([np.inf, -np.inf], np.nan, inplace=True)

    return model_data

# Example usage:
if __name__ == "__main__":

    print()
    print("####PREPROCESS DATA####")
    find_and_append_module_path()
    # Import necessary configurations
    import config as CONFIG
    from src.features import load_team_opponent
    from src.features.preprocess import derived_odds,get_bookmaker, get_odd_pred_team_opponent, split_date

    print("load raw data...")
    # Load your data into df here
    df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
    
    print("preprocess data...")
    processed_data = preprocess_data(df)

    print("save model data...")
    processed_data.to_csv(CONFIG.DATA_FOLDER_PROCESSED + 'model_data_deployment.csv')
    print('Done')
