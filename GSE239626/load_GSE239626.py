import os

import pandas as pd
import scipy.io

from utils import (decompress_gzip, load_data_from_link, load_pickle,
                   save_piclke, unzip_file)

FOLDER_PATH = 'GSE239626/'

FEATURES_ZIP_PATH = 'GSE239626/GSE239626_features.zip'
FEATURES_PATH = 'GSE239626/features.tsv'
MATRIX_PATH = 'GSE239626/GSE239626_matrix.mtx'
MATRIX_LINK = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE239nnn/GSE239626/suppl/GSE239626_matrix.mtx.gz'
BARCODE_ZIP_PATH = 'GSE239626/GSE239626_barcode.zip'
BARCODE_PATH = 'GSE239626/GSE239626_barcode.tsv'

GENOMIC_MATRIX_PATH = 'GSE239626\GSE239626_genomic_matrix_matrix.pkl'
GENE_EXPRESSION_PATH = 'GSE239626\GSE239626_gene_expression_matrix.pkl'
ANTIBODY_CAPTURE_PATH = 'GSE239626\GSE239626_antibody_capture_matrix.pkl'

FAMILY_ZIP_PATH = 'GSE239626/GSE239626_family_phenotype_data.zip'
FAMILY_PATH = 'GSE239626/GSE239626_family_phenotype_data.pkl'


def slip_antibody_and_gene(genomic_matrix_df):
    antibody_capture_df = genomic_matrix_df[genomic_matrix_df['expression'] == 'Antibody Capture']
    gene_expression_df = genomic_matrix_df[genomic_matrix_df['expression'] == 'Gene Expression']

    save_piclke(antibody_capture_df, ANTIBODY_CAPTURE_PATH)
    save_piclke(gene_expression_df, GENE_EXPRESSION_PATH)

def assemble_genomic_matrix():
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

    save_piclke(genomic_matrix_df, GENOMIC_MATRIX_PATH)

def load_genomic_matrix():
    if os.path.exists(GENOMIC_MATRIX_PATH):
        genomic_matrix_df = load_pickle(GENOMIC_MATRIX_PATH)
    else:
        assemble_genomic_matrix()
        genomic_matrix_df = load_pickle(GENOMIC_MATRIX_PATH)

    if os.path.exists(GENE_EXPRESSION_PATH) and os.path.exists(ANTIBODY_CAPTURE_PATH):
        gene_expression_df = load_pickle(GENE_EXPRESSION_PATH)
        antibody_capture_df = load_pickle(ANTIBODY_CAPTURE_PATH)
    else:
        slip_antibody_and_gene(genomic_matrix_df)
    
    return genomic_matrix_df, gene_expression_df, antibody_capture_df

def load_GSE239626():
    genomic_matrix_df, gene_expression_df, antibody_capture_df = load_genomic_matrix()
    unzip_file(FAMILY_ZIP_PATH)
    family_phenotype_df = pd.read_pickle(FAMILY_PATH)

    return genomic_matrix_df, gene_expression_df, antibody_capture_df, family_phenotype_df