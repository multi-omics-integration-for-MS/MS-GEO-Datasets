import glob
import gzip
import os
import zipfile

import pandas as pd
import requests


def load_data_from_link(url, folder_path):
    if os.path.exists(folder_path+url.split("/")[-1]):
        # File already exists
        return folder_path+url.split("/")[-1]
    else:
        response = requests.get(url)
        filename = folder_path+url.split("/")[-1]

        with open(filename, 'wb') as f:
            f.write(response.content)

        return filename

def unzip_file(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        folder_path = os.path.dirname(zip_path)
        zip_ref.extractall(folder_path)

    #unzip_file = zip_ref.namelist()
    #return unzip_file

def unzip_and_extract_file(zip_path, file_path):
    if not os.path.exists(file_path):
        unzip_file(zip_path)
    df = pd.read_csv(file_path, index_col=0)

    return df

def decompress_gzip(input_filepath, output_filepath):
    input_files = glob.glob(input_filepath)

    for f_path in input_files:
        with gzip.open(f_path, 'rb') as f_in:
            with open(output_filepath, 'wb') as f_out:
                f_out.write(f_in.read())

def save_piclke(df, path):
    df.to_pickle(path)

def load_pickle(path):
    return pd.read_pickle(path)