import os
import shutil
import sys

# Directories
ROOT_FOLDER = os.getcwd()
if ROOT_FOLDER == "{parent}":
    ROOT_FOLDER = "./"


TEMP_FOLDER = ROOT_FOLDER +  '/tmp/'
PNG_FOLDER = TEMP_FOLDER + '/png/'
OUT_FOLDER = ROOT_FOLDER+  '/out/'
PDF_FOLDER = OUT_FOLDER + '/pdf/'
JSON_FOLDER = OUT_FOLDER +  '/json/'
PIC_FOLDER = OUT_FOLDER +  '/pic/'
MODEL_FOLDER = OUT_FOLDER +  '/model/'
SCRIPT_FOLDER = ROOT_FOLDER + "/scripts/"
LOG_FOLDER = SCRIPT_FOLDER + "/logs/"


# Data Folder
DATA_FOLDER = ROOT_FOLDER + '/data/'
DATA_FOLDER_RAW = DATA_FOLDER + '/raw/'
DATA_FOLDER_PROCESSED = DATA_FOLDER +  '/processed/'
DATA_FOLDER_MAPPING = DATA_FOLDER + '/mapping/'
DATA_FOLDER_MODELS = DATA_FOLDER + '/models/'

NUMBER_OF_GAMES = 3

MAIN_LEAGUES = ["D1", "F1", "I1", "E0", "E1", "E2", "E3", "SP1", "D2", "F2", "SP2", "I2", "N1", "SC0", "B1", "P1", "T1", "G1"]
SEASONS =  ["1213","1314","1415","1516","1617","1718","1819","1920","2021","2122","2223","2324"]
ATTRIBUTES_MAIN_LEAGUE = ['AC','AF','AHCh','AHh','AR','AS','AST','AY','Avg<2.5','Avg>2.5','AvgA','AvgAHA','AvgAHH','AvgC<2.5','AvgC>2.5','AvgCA','AvgCAHA','AvgCAHH','AvgCD','AvgCH','AvgD','AvgH','AwayTeam','B365<2.5','B365>2.5','B365A','B365AHA','B365AHH','B365C<2.5','B365C>2.5','B365CA','B365CAHA','B365CAHH','B365CD','B365CH','B365D','B365H','BWA','BWCA','BWCD','BWCH','BWD','BWH','Date','Div','FTAG','FTHG','FTR','HC','HF','HR','HS','HST','HTAG','HTHG','HTR','HY','HomeTeam','IWA','IWCA','IWCD','IWCH','IWD','IWH','Max<2.5','Max>2.5','MaxA','MaxAHA','MaxAHH','MaxC<2.5','MaxC>2.5','MaxCA','MaxCAHA','MaxCAHH','MaxCD','MaxCH','MaxD','MaxH','P<2.5','P>2.5','PAHA','PAHH','PC<2.5','PC>2.5','PCAHA','PCAHH','PSA','PSCA','PSCD','PSCH','PSD','PSH','Time','VCA','VCCA','VCCD','VCCH','VCD','VCH','WHA','WHCA','WHCD','WHCH','WHD','WHH']

EXTRA_LEAGUES = ["ARG", "AUT", "BRA", "CHN", "DNK", "FIN", "IRL", "JPN", "MEX", "NOR", "POL", "ROU", "RUS", "SWE", "SWZ", "USA"]
ATTRIBITES_EXTRA_LEAGUE = ['Country', 'League', 'Season', 'Date', 'Time', 'Home', 'Away', 'HG', 'AG', 'Res', 'PH', 'PD', 'PA', 'MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA']
