import logging
import os
import sys
import pandas as pd

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

if __name__ == "__main__":
    import config as CONFIG
    from scripts.process_data.preprocess_team_opponent_deployment import (
        load_team_opponent, preprocess_data)
    from src.data.provide_data import get_model_data
    from src.deploy.results import transform_and_merge
    # Configure logging
    print("File:",os.getcwd())
    # print("Dirs",os.listdir())
    # Create a StreamHandler to also log to the console
    print("find_and_append_module_path...")
    find_and_append_module_path()
    print("File:",os.getcwd())
    
    print("Load Data...")
    df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_FIXTURES+"update.csv")
    print("Predict Matches...")
    predict_matches(df = df)
    print("sucessfully predicted")
