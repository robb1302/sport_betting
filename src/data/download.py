import os
import pandas as pd
import config as CONFIG
import sys

def download_season(season:list,leagues:list):
    """
    The function downloads given season
    """
    print("season", season)

    for league in leagues:
        print(league)
        #updateMarktwerte(liga = LIGA)
        try:
            downloadLeague(liga=league, season=season)
        except:
            print("Fehler in Liga: ", league)
            print("Unexpected error:", sys.exc_info()[0])
            pass



def readSchedule(liga="D1"):
    main_path = "C:/Users/Robert/Documents/Projekte/workspace/python/bettingTool/src/leagues/"
    os.chdir(main_path + liga)
    dataframe = pd.read_excel("schedule.xlsx", header=None) 
    output = liga + " wurde erfolgreich eingelesen."
    print(output)  
    return(pd.DataFrame(dataframe))


def downloadLeague(liga="D1", season="1920"):
    if liga in CONFIG.MAIN_LEAGUES:
        url = 'https://www.football-data.co.uk/mmz4281/' + season + '/' + liga + '.csv'
    elif CONFIG.EXTRA_LEAGUES:
        url = f'https://www.football-data.co.uk/new/{liga}.csv'

    data = pd.read_csv(url, sep=",", encoding='cp1252')  # use sep="," for coma separation. 
    main_path =CONFIG.DATA_FOLDER_RAW
    data.to_csv(main_path + liga + '/season/' + liga + '_' + season + '.csv')
    return(data)

def download_fixtures( url:str = "https://www.football-data.co.uk/fixtures.csv"):
    
    print("start downloading fixtures...")
    try:
        data = pd.read_csv(url, sep=",", encoding='cp1252')   # use sep="," for coma separation. 
    except:
        raise ValueError(f"{url} can't be downloaded")
    
    if not os.path.exists(CONFIG.DATA_FOLDER_FIXTURES):
        FileNotFoundError(f"The file or directory '{CONFIG.DATA_FOLDER_FIXTURES}' does not exist.")
    else:
        data.to_csv(CONFIG.DATA_FOLDER_FIXTURES+'update.csv')
        print("succesfull updated fixtures")

@DeprecationWarning
# Liest zu einer festgelegten Saison einer gewaehlten Liga die Saisondaten ein
def readLeague(liga="D1", season="1920"):
    main_path = CONFIG.DATA_FOLDER+"/src/leagues/"
    os.chdir(main_path + liga + "/season")
    dataframe = pd.read_csv(liga + "_" + season + ".csv") 
    return dataframe

@DeprecationWarning
def download_next_matchday():
    url = 'https://www.football-data.co.uk/fixtures.csv'
    data = pd.read_csv(url, sep=",", encoding='cp1252', error_bad_lines=False)
    main_path = CONFIG.DATA_FOLDER+"/leagues/"

    data.to_csv(main_path + 'next_matchday.csv')

