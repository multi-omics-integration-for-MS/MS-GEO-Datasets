import pandas as pd
import scipy.io

from utils import decompress_gzip, load_data_from_link, unzip_file

FOLDER_PATH = 'GSE239626/'

FEATURES_ZIP_PATH = 'GSE239626/GSE239626_features.zip'
FEATURES_PATH = 'GSE239626/features.tsv'

MATRIX_PATH = 'GSE239626/GSE239626_matrix.mtx'
MATRIX_LINK = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE239nnn/GSE239626/suppl/GSE239626_matrix.mtx.gz'

BARCODE_ZIP_PATH = 'GSE239626/GSE239626_barcode.zip'
BARCODE_PATH = 'GSE239626/GSE239626_barcode.tsv'

FAMILY_ZIP_PATH = 'GSE239626/GSE239626_family_phenotype_data.zip'
FAMILY_PATH = 'GSE239626/GSE239626_family_phenotype_data.pkl'


def load_genomic_matrix():
    unzip_file(FEATURES_ZIP_PATH)
    features_df = pd.read_csv(FEATURES_PATH, sep='\t', header=None)
    features_df.columns = ['ID', 'symbol', 'expression']

    matrix_gzip_path = load_data_from_link(MATRIX_LINK, FOLDER_PATH)
    decompress_gzip(matrix_gzip_path, MATRIX_PATH)
    matrix = scipy.io.mmread(MATRIX_PATH)
    matrix_df = pd.DataFrame.sparse.from_spmatrix(matrix)
    
    unzip_file(BARCODE_ZIP_PATH)
    barcode_df = pd.read_csv(BARCODE_PATH, header=None)

    matrix_df.columns = barcode_df[0]
    genomic_matrix_df = pd.concat([features_df, matrix_df], axis=1)

    return genomic_matrix_df

def load_GSM7669046():
    genomic_matrix_df = load_genomic_matrix()
    unzip_file(FAMILY_ZIP_PATH)
    family_phenotype_df = pd.read_pickle(FAMILY_PATH)

    return genomic_matrix_df, family_phenotype_df