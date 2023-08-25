import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace('scripts','')
sys.path.append(parent_dir)

import os
import pandas as pd
import time
import logging
from src.utils.utils import load_from_pickle
import config as CONFIG

# Configure the logger
logging.basicConfig(filename=CONFIG.LOG_FOLDER+'data_preprocessing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    try:
        logging.info('Loading data from pickle file...')
        df = load_from_pickle(CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
        return df
    except Exception as e:
        logging.error(f"An error occurred while loading data: {str(e)}")
        return None

def preprocess_data(df):
    try:
        logging.info('Start data preprocessing...')
        
        # Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

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

        logging.info('Data preprocessing completed.')
        return df
    except Exception as e:
        logging.error(f"An error occurred during data preprocessing: {str(e)}")
        return None

def save_processed_data(df):
    try:
        logging.info('Saving processed data to CSV...')

        # Create a timestamp for the output file
        timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")

        # Define the output file path with the timestamp
        # output_file = os.path.join(CONFIG.DATA_FOLDER_PROCESSED, f'model_data_{timestamp}.csv')
        output_file = os.path.join(CONFIG.DATA_FOLDER_PROCESSED, f'model_data.csv')


        # Save the processed data to the CSV file
        df.to_csv(output_file)

        logging.info(f'Processed data saved to {output_file}.')
    except Exception as e:
        logging.error(f"An error occurred while saving processed data: {str(e)}")

def main():
    try:
        logging.info('Data preprocessing script started.')
        
        # Record the start time
        start_time = time.time()
        
        # Load the data
        data = load_data()
        
        if data is not None:
            # Preprocess the data
            processed_data = preprocess_data(data)
            
            if processed_data is not None:
                # Save the processed data
                save_processed_data(processed_data)
                
                # Calculate and log the execution time
                end_time = time.time()
                execution_time = end_time - start_time
                logging.info(f'Script execution completed. Execution time: {execution_time:.2f} seconds')
        
        logging.info('Data preprocessing script finished.')
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
