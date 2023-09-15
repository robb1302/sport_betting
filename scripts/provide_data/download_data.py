# Download update data and saves as pickle
# TODO: saves Fixtures
# TODO: preprocess and save

import os
import sys
import argparse
import tqdm
from os import listdir
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

def download_raw_data(league=None, season=None):
    import config as CONFIG
    if type(season) is str:
        season = [season]

    if type(league) is str:
        league = [league]  

    from src.utils.utils import createDirs
    from src.data.download import downloadLeague
 
    try:
        os.makedirs(CONFIG.DATA_FOLDER_RAW, exist_ok=True)


        for liga in tqdm.tqdm(league):
            createDirs(liga=liga, data_path=CONFIG.DATA_FOLDER_RAW)
            for s in season:
                try:
                    downloadLeague(liga=liga, season=s)
                except Exception as e:
                    print(f"Error processing {liga}, {s}: {str(e)}")
                    continue

        leagues_folder = CONFIG.DATA_FOLDER_RAW
        data = pd.DataFrame(columns = list(set(CONFIG.ATTRIBUTES_MAIN_LEAGUE+CONFIG.ATTRIBITES_EXTRA_LEAGUE)))
        
        for l in tqdm.tqdm(league):
            if os.path.exists(f"{leagues_folder}/{l}/season/"):
                seasons = listdir(f"{leagues_folder}/{l}/season/")
                for s in seasons:
        
                    df = pd.read_csv(f"{leagues_folder}/{l}/season/{s}",index_col=0)
                    data = pd.concat([df,data],axis=0)


        data = data.drop([i for i in data.columns if 'unnamed' in i.lower()],axis=1)
        data = data.drop_duplicates()
        
        
        import pickle

        filename_main = CONFIG.DATA_FOLDER_RAW+'raw_database.sav'
        pickle.dump(data, open(filename_main, 'wb'))

        filename_main = CONFIG.DATA_FOLDER_RAW+'main_leagues_database_raw.sav'
        pickle.dump(data[~data.HomeTeam.isna()][CONFIG.ATTRIBUTES_MAIN_LEAGUE], open(filename_main, 'wb'))

        filename_extra = CONFIG.DATA_FOLDER_RAW+'extra_leagues_database_raw.sav'
        pickle.dump(data[data.HomeTeam.isna()][CONFIG.ATTRIBITES_EXTRA_LEAGUE], open(filename_extra, 'wb'))

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    find_and_append_module_path()
    import config as CONFIG
    
    parser = argparse.ArgumentParser(description="Download data for a specific league and season.")
    parser.add_argument("--league", help="Specify the league to download data for (e.g., 'EPL').",default=CONFIG.MAIN_LEAGUES)
    parser.add_argument("--season", help="Specify the season to download data for (e.g., '2324').",default="2324")
    args = parser.parse_args()

    download_raw_data(args.league, args.season)
