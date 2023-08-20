import os
import sys
import tqdm


# Get the current working directory
current_directory = os.getcwd()
# Define the substring to find
substring_to_find = 'sport_betting'
# Use str.find() to find the position of the substring
index = current_directory.find(substring_to_find)
parent_dir = f"{ current_directory[0:index]}/{substring_to_find}"
sys.path.append(parent_dir)

from src.utils.utils import createDirs
import config as CONFIG
from src.data.download import downloadLeague

def update_league(liga="D1", season="1920"):
    if liga in CONFIG.MAIN_LEAGUES:
        url = 'https://www.football-data.co.uk/mmz4281/fixtures.csv'

    data = pd.read_csv(url, sep=",", encoding='cp1252', error_bad_lines=False)  # use sep="," for coma separation. 
    main_path =CONFIG.DATA_FOLDER_RAW
    data.to_csv('update.csv')
    return(data)

pd.read_csv('https://www.football-data.co.uk/fixtures.csv', sep=",", encoding='cp1252', error_bad_lines=False)  