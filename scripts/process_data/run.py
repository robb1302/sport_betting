import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace('scripts','')
sys.path.append(parent_dir)

import sys
import os
import time
import logging
import pandas as pd
import numpy as np
from src.utils.utils import createDirs
import config as CONFIG
from src.features import load_team_opponent
from src.features.preprocess import (
    derived_odds,
    get_bookmaker,
    get_odd_pred_team_opponent,
    split_date,
    add_last_3_scores_column
)
def setup_logger():
    logging.basicConfig(filename=CONFIG.LOG_FOLDER + 'data_preprocessing.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        setup_logger()
        logging.info('Data preprocessing script started.')
        
        # Record the start time
        start_time = time.time()
        
        # Load data
        df = load_team_opponent(filename_main=CONFIG.DATA_FOLDER_RAW + 'main_leagues_database_raw.sav')
        df = split_date(df)
        df = df.sort_values(['year', 'month', 'day'], ascending=False).reset_index()

        # Extract attributes
        logging.info('Extract bookmaker attributes...')
        standad_attributes = ['Target', 'atHome', 'Date', 'Div']
        bookmaker_attributes = (
            get_bookmaker(bm='BW', df=df) +
            get_bookmaker(bm='B365', df=df) +
            get_bookmaker(bm='IW', df=df)
        )
        bet_on_team = get_bookmaker(bm='Team', df=df[bookmaker_attributes])
        bet_on_opponent = get_bookmaker(bm='Opponent', df=df[bookmaker_attributes])
        bet_on_draw = get_bookmaker(bm='Draw', df=df[bookmaker_attributes])

        # Generate derived odds
        logging.info('Generate derived odds...')
        df_derived_b365 = get_odd_pred_team_opponent(bet="B365", df=df)
        df_derived_iw = get_odd_pred_team_opponent(bet="IW", df=df)
        df_derived_bw = get_odd_pred_team_opponent(bet="BW", df=df)
        df_derived_team = derived_odds(sight='Team', df=df, odds=bet_on_team)
        df_derived_opponent = derived_odds(sight='Opponent', df=df, odds=bet_on_opponent)
        df_derived_draw = derived_odds(sight='Draw', df=df, odds=bet_on_draw)

        # Calculate differences
        logging.info('Calculate differences...')
        df["diff_FTG_against_Opponent"] = df["FTG_Team"] - df["FTG_Opponent"]
        df["diff_ShotsOnTarget_against_Opponent"] = df["ShotsOnTarget_Team"] - df["ShotsOnTarget_Opponent"]

        # Add rolling means
        # columns_to_roll = ["diff_FTG_against_Opponent", "diff_ShotsOnTarget_against_Opponent", "B365_Team", "B365_Opponent"]
        # for col in columns_to_roll:
        #     df = add_last_3_scores_column(df=df, score_column=col, anz_games=4)

        # Set 'Target' column
        df['Target'] = df.FTG_Team > df.FTG_Opponent

        # Drop NaN rows
        df = df.dropna()

        # Concatenate data
        rolling_mean_attributes = [c for c in df.columns if 'last' in c]
        model_data = pd.concat([df[rolling_mean_attributes], df[standad_attributes], df[bookmaker_attributes],
                                df[["Team", "month", "year"]], df_derived_team, df_derived_opponent,
                                df_derived_draw, df_derived_b365, df_derived_iw, df_derived_bw], axis=1)

        # Replace inf and -inf with NaN
        model_data.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Save to CSV
        model_data.to_csv(CONFIG.DATA_FOLDER_PROCESSED + 'model_data_all.csv')
        
        # Calculate and log the execution time
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f'Script execution completed. Execution time: {execution_time:.2f} seconds')
        print('Done')

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()