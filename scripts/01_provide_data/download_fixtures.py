import os
import sys
import tqdm
import pandas as pd

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

def download_fixtures(    url:str = "https://www.football-data.co.uk/fixtures.csv"):
    data = pd.read_csv(url, sep=",", encoding='cp1252')   # use sep="," for coma separation. 
    data.to_csv(CONFIG.DATA_FOLDER_RAW+'fixtures/update.csv')
    return(data)
download_fixtures(url = "https://www.football-data.co.uk/fixtures.csv")
print('Done')
pd.read_csv('https://www.football-data.co.uk/fixtures.csv', sep=",", encoding='cp1252')  