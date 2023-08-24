import os
import shutil
import sys

# Directories
ROOT_FOLDER = os.getcwd()


# Function to create a directory if it doesn't exist
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

TEMP_FOLDER = ROOT_FOLDER + '/tmp/'
create_directory_if_not_exists(TEMP_FOLDER)

PNG_FOLDER = TEMP_FOLDER + '/png/'
create_directory_if_not_exists(PNG_FOLDER)

OUT_FOLDER = ROOT_FOLDER + '/out/'
create_directory_if_not_exists(OUT_FOLDER)

PDF_FOLDER = OUT_FOLDER + '/pdf/'
create_directory_if_not_exists(PDF_FOLDER)

JSON_FOLDER = OUT_FOLDER + '/json/'
create_directory_if_not_exists(JSON_FOLDER)

PIC_FOLDER = OUT_FOLDER + '/pic/'
create_directory_if_not_exists(PIC_FOLDER)

MODEL_FOLDER = OUT_FOLDER + '/model/'
create_directory_if_not_exists(MODEL_FOLDER)

SCRIPT_FOLDER = ROOT_FOLDER + "/scripts/"
create_directory_if_not_exists(SCRIPT_FOLDER)

LOG_FOLDER = SCRIPT_FOLDER + "/logs/"
create_directory_if_not_exists(LOG_FOLDER)

# Data Folder
DATA_FOLDER = ROOT_FOLDER + '/data/'
create_directory_if_not_exists(DATA_FOLDER)

DATA_FOLDER_RAW = DATA_FOLDER + '/raw/'
create_directory_if_not_exists(DATA_FOLDER_RAW)

DATA_FOLDER_FIXTURES = DATA_FOLDER + '/fixtures/'
create_directory_if_not_exists(DATA_FOLDER_FIXTURES)

DATA_FOLDER_PROCESSED = DATA_FOLDER + '/processed/'
create_directory_if_not_exists(DATA_FOLDER_PROCESSED)

DATA_FOLDER_MAPPING = DATA_FOLDER + '/mapping/'
create_directory_if_not_exists(DATA_FOLDER_MAPPING)

DATA_FOLDER_MODELS = DATA_FOLDER + '/models/'
create_directory_if_not_exists(DATA_FOLDER_MODELS)


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
