import os
import pickle
import zipfile

import pandas as pd


def load_df(df_zip_path, file_format='pickle'):
    with zipfile.ZipFile(df_zip_path, 'r') as zip_ref:
        folder_path = os.path.dirname(df_zip_path)
        zip_ref.extractall(folder_path)

    if file_format == 'pickle':
        file_ext = '.pkl'
        file_path = df_zip_path.replace('.zip', file_ext)
        with open(file_path, 'rb') as file:
            df = pickle.load(file)
    elif file_format == 'csv':
        file_ext = '.csv'
        file_path = df_zip_path.replace('.zip', file_ext)
        df = pd.read_csv(file_path)

    return df

