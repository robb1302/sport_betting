import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from src.utils.utils import createDirs
import config as CONFIG
from src.data.download import downloadLeague


LIGA = ["D1", "F1", "I1", "E0", "E1","E2","E3", "SP1", "D2", "F2", "SP2", "I2", "N1", "SC0", "B1", "P1", "T1", "G1"]
SEASONS = ["2223"]

for liga in CONFIG.MAIN_LEAGUES:
    createDirs(liga=liga, data_path=CONFIG.DATA_FOLDER_RAW)
    for s in CONFIG.SEASONS:
        try:
            downloadLeague(liga=liga, season = s)
        except:
            pass
#downloadLineupsLeague(1,300,LIGA)
#downloadLeagueValue(yearStart=2014,yearEnd = 2020, Ligen=["E0"])
