import os

from utils import unzip_and_extract_file

REPOSITORY_PATH = 'MS-GEO-Datasets/'

MATRIX_ZIP_PATH = 'GSE159033/GSE159033_genomic_matrix.zip'
MATRIX_PATH = 'GSE159033/GSE159033_genomic_matrix_matrix.csv'

FAMILY_ZIP_PATH = 'GSE159033/GSE159033_family_phenotype_data.zip'
FAMILY_PATH = 'GSE159033/GSE159033_family_phenotype_data.csv'


def load_GSE159033():
    """
    Load data from GSE159033 dataset

    Returns:
        genomic_matrix_df (pd.DataFrame): Genomic matrix data
        family_phenotype_df (pd.DataFrame): Family phenotype data
    """
    if REPOSITORY_PATH in os.getcwd(): root = REPOSITORY_PATH
    else: root = ''

    genomic_matrix_df = unzip_and_extract_file(root+MATRIX_ZIP_PATH, MATRIX_PATH)
    family_phenotype_df = unzip_and_extract_file(root+FAMILY_ZIP_PATH, FAMILY_PATH)

    return genomic_matrix_df, family_phenotype_df