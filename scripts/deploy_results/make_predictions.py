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

    # Initialize scaler object
    scaler = pickle.load(open(CONFIG.DATA_FOLDER_MODELS+"scaler_team_opponent.pkl","rb"))
    df_scaled = scaler.transform(df[scaler.feature_names_in_])

    clf = pickle.load(open(CONFIG.DATA_FOLDER_MODELS+"xgb.pkl","rb"))
    preds = pd.DataFrame(clf.predict_proba(df_scaled)[:,1],columns=["preds"])

    result_df = transform_and_merge(df = df, preds=preds)
    result_df["Fair Home Odd"] = round(1/result_df.preds_home,2)
    result_df["Fair Draw Odd"] = round( 1/result_df.preds_draw,2)
    result_df["Fair Away Odd"] = round( 1/result_df.preds_away,2)

    result_df.preds_home = round(result_df.preds_home,2)
    result_df.preds_draw = round(result_df.preds_draw,2)
    result_df.preds_away = round(result_df.preds_away,2)

    # Rename the columns based on the specified dictionary
    rename_columns = {
        "Home": "Home Team",
        "Away": "Away Team",
        "preds_home": "Home Prob",
        "preds_draw": "Draw Prob",
        "preds_away": "Away Prob"
    }

    # Rename the DataFrame columns
    result_df.columns = [rename_columns.get(col, col) for col in result_df.columns]
    return result_df

if __name__ == "__main__":
    print()
    print("####PREDICT OUTCOME#####")
    # Configure logging
    print("File:",os.getcwd())

    # Create a StreamHandler to also log to the console
    print("find_and_append_module_path...")
    find_and_append_module_path()
    
    import config as CONFIG
    from scripts.process_data.preprocess_team_opponent_deployment import (
        load_team_opponent, preprocess_data)
    from src.deploy.results import transform_and_merge

    print("Load Data...")
    df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_FIXTURES+"update.csv")
    print("Predict Matches...")
    result_df = predict_matches(df = df)
    result_df.to_csv(f"{CONFIG.DATA_FOLDER_RESULTS}results.csv")
    print("sucessfully predicted")
