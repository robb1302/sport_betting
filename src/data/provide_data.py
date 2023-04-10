import pandas as pd
import config as CONFIG

def get_model_data(filename:str):
    """
    Funktion lädt Modeldataset 
    """
    model_data = pd.read_csv(CONFIG.DATA_FOLDER_PROCESSED+f"/{filename}/model_data.csv",index_col=0)
    model_data = model_data.select_dtypes(exclude='object')
    model_data = model_data.dropna()
    y = model_data['Target']
    X = model_data.drop(['Target'], axis=1)
    print(filename, len(y))
    return X,y