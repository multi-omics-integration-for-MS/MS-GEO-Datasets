import os
import zipfile

import pandas as pd


def load_df(df_zip_path):
    with zipfile.ZipFile(df_zip_path, 'r') as zip_ref:
        folder_path = os.path.dirname(df_zip_path)
        zip_ref.extractall(folder_path)
    csv_path = df_zip_path.replace('.zip', '.csv')
    df = pd.read_csv(csv_path)

    return df