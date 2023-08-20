import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace('scripts','')
sys.path.append(parent_dir)

import pandas as pd
from src.utils.utils import load_from_pickle
import config as CONFIG
import time

def preprocess_data():
    print('Start')
    
    start_time = time.time()  # Record the start time
    
    # Load data from pickle file
    df = load_from_pickle(CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
    
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Reset the index
    df = df.reset_index()

    # Load data again (repeated)
    df = load_from_pickle(source_path=CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
    
    # Filter out rows with missing values in the 'FTR' column
    df = df[~df.FTR.isna()]

    bet_attributes = ['IWH', 'IWD', 'IWA', 'BWH', 'BWD', 'BWA', 'B365H', 'B365D', 'B365A']
    
    # Convert 'Date' column to datetime format again
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Check for rows with complete betting data
    complete_bets = df[bet_attributes].isna().T.sum() == 0
    df = df[complete_bets]

    X = df[["HomeTeam", "AwayTeam", "Div", "B365H", "B365D", "B365A", "BWH", "BWD", "BWA", "IWH", "IWD", "IWA"]]
    X.head()

    y = df[["B365H", "B365D", "B365A", "FTR"]]
    y.columns = ["H", "D", "A", "R"]

    def make_y(y_row):
        r = y_row["R"]
        y_row[r] = y_row[r] - 1
        results = {'H', 'D', 'A'}
        y_row[list(results - {r})] = 0
        return y_row

    # Apply the make_y function to every row of the DataFrame
    y = y.apply(lambda x: make_y(x), axis=1)
    df = pd.concat([X, y], axis=1)
    
    # Save the processed data to a CSV file
    df.to_csv(CONFIG.DATA_FOLDER_PROCESSED + 'model_data.csv')
    
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time
    print(f"Done. Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    preprocess_data()
