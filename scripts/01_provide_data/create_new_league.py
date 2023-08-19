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

for liga in tqdm.tqdm(CONFIG.MAIN_LEAGUES):
    createDirs(liga=liga, data_path=CONFIG.DATA_FOLDER_RAW)
    for s in CONFIG.SEASONS:
        try:
            downloadLeague(liga=liga, season = s)
        except Exception as e:
            print("Error:"e,"\n",liga,s)
            pass

