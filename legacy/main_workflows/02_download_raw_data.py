import os
import sys
import argparse
import tqdm
from os import listdir
import pandas as pd

def find_and_append_module_path():
    current_directory = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_directory.find(substring_to_find)
    
    if index != -1:
        parent_dir = os.path.join(current_directory[:index], substring_to_find)
        sys.path.append(parent_dir)

def main(league=None, season=None):
    find_and_append_module_path()

    # Now that the path is set, import modules that depend on it
    import config as CONFIG
    from src.utils.utils import createDirs
    from src.data.download import downloadLeague

    try:
        os.makedirs(CONFIG.DATA_FOLDER_RAW, exist_ok=True)

        leagues = [league] if league else CONFIG.MAIN_LEAGUES
        seasons = [season] if season else CONFIG.SEASONS

        for liga in tqdm.tqdm(leagues):
            createDirs(liga=liga, data_path=CONFIG.DATA_FOLDER_RAW)
            for s in seasons:
                try:
                    downloadLeague(liga=liga, season=s)
                except Exception as e:
                    print(f"Error processing {liga}, {s}: {str(e)}")
                    continue

        leagues = listdir(CONFIG.DATA_FOLDER_RAW)
        leagues_folder = CONFIG.DATA_FOLDER_RAW
        data = pd.DataFrame(columns = list(set(CONFIG.ATTRIBUTES_MAIN_LEAGUE+CONFIG.ATTRIBITES_EXTRA_LEAGUE)))
        import pandas as pd
        for l in tqdm(leagues):
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
    parser = argparse.ArgumentParser(description="Download data for a specific league and season.")
    parser.add_argument("--league", help="Specify the league to download data for (e.g., 'EPL').")
    parser.add_argument("--season", help="Specify the season to download data for (e.g., '2324').")
    args = parser.parse_args()

    main(args.league, args.season)
