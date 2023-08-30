
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
import logging

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
from src.data.provide_data import get_model_data
from scripts.process_data.preprocess_team_opponent_deployment import preprocess_data,load_team_opponent
from src.deploy.results import transform_and_merge

def predict_matches(df):


    # TODO: Include neede Columns
    df = df[~df.WH_Team.isna()]
    df = preprocess_data(df)

    import pickle
    clf = pickle.load(open(CONFIG.DATA_FOLDER_MODELS+"xgb.pkl","rb"))

    X_train, _ = get_model_data(filename = "train",model_data="model_data",use_categories=False)


    # TODO: Import scaler
    from sklearn.preprocessing import StandardScaler

    # Initialize scaler object
    scaler = StandardScaler()

    # Fit scaler on training data
    scaler.fit(X_train)
    df_scaled = scaler.transform(df[X_train.columns])

    preds = pd.DataFrame(clf.predict_proba(df_scaled)[:,1],columns=["preds"])

    result_df = transform_and_merge(df = df, preds=preds)

    
    return result_df

# Example usage:
if __name__ == "__main__":
    # Load your data into df here
    df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_FIXTURES+"update.csv")
    
    result_df = predict_matches(df = df)
    result_df.to_csv(CONFIG.DATA_FOLDER_RESULTS+'results.csv')
    print('Done')