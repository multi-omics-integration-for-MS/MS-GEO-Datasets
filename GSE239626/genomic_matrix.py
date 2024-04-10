import zipfile

import pandas as pd


def read_matrix_from_zip(zip_path, matrix_name):
    with zipfile.ZipFile(zip_path) as zip_file:
        with zip_file.open(matrix_name) as matrix_file:
            return pd.read_csv(matrix_file, sep='\t', index_col=0)

def concatenate_matrices(zip_paths, matrix_name):
    matrices = [read_matrix_from_zip(zip_path, matrix_name) for zip_path in zip_paths]
    return pd.concat(matrices, axis=1)