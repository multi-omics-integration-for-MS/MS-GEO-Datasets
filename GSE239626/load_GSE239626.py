import os

import pandas as pd
import scipy.io

from utils import (decompress_gzip, load_data_from_link, load_pickle,
                   save_piclke, unzip_file)

REPOSITORY_PATH = 'MS-GEO-Datasets/'
FOLDER_PATH = 'GSE239626/'

FEATURES_ZIP_PATH = 'GSE239626/GSE239626_features.zip'
FEATURES_PATH = 'GSE239626/features.tsv'
MATRIX_PATH = 'GSE239626/GSE239626_matrix.mtx'
MATRIX_LINK = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE239nnn/GSE239626/suppl/GSE239626_matrix.mtx.gz'
BARCODE_ZIP_PATH = 'GSE239626/GSE239626_barcode.zip'
BARCODE_PATH = 'GSE239626/GSE239626_barcode.tsv'

GENOMIC_MATRIX_PATH = 'GSE239626/GSE239626_genomic_matrix.pkl'
GENE_EXPRESSION_PATH = 'GSE239626/GSE239626_gene_expression_matrix.pkl'
ANTIBODY_CAPTURE_PATH = 'GSE239626/GSE239626_antibody_capture_matrix.pkl'

FAMILY_ZIP_PATH = 'GSE239626/GSE239626_family_phenotype_data.zip'
FAMILY_PATH = 'GSE239626/GSE239626_family_phenotype_data.pkl'


def split_antibody_and_gene(genomic_matrix_df, root):
    antibody_capture_df = genomic_matrix_df[genomic_matrix_df['expression'] == 'Antibody Capture']
    gene_expression_df = genomic_matrix_df[genomic_matrix_df['expression'] == 'Gene Expression']

    save_piclke(antibody_capture_df, root+ANTIBODY_CAPTURE_PATH)
    save_piclke(gene_expression_df, root+GENE_EXPRESSION_PATH)

def assemble_genomic_matrix(root):
    if not os.path.exists(root+FEATURES_PATH):
        unzip_file(root+FEATURES_ZIP_PATH)
    features_df = pd.read_csv(root+FEATURES_PATH, sep='\t', header=None)
    features_df.columns = ['ID', 'symbol', 'expression']

    matrix_gzip_path = load_data_from_link(MATRIX_LINK, root+FOLDER_PATH)
    decompress_gzip(matrix_gzip_path, root+MATRIX_PATH)
    matrix = scipy.io.mmread(root+MATRIX_PATH)
    matrix_df = pd.DataFrame.sparse.from_spmatrix(matrix)
    
    if not os.path.exists(root+BARCODE_PATH):
        unzip_file(root+BARCODE_ZIP_PATH)
    barcode_df = pd.read_csv(root+BARCODE_PATH, header=None)

    matrix_df.columns = barcode_df[0]
    genomic_matrix_df = pd.concat([features_df, matrix_df], axis=1)

    save_piclke(genomic_matrix_df, root+GENOMIC_MATRIX_PATH)

def load_genomic_matrix(root):
    if os.path.exists(root+GENOMIC_MATRIX_PATH):
        genomic_matrix_df = load_pickle(root+GENOMIC_MATRIX_PATH)
    else:
        assemble_genomic_matrix(root)
        genomic_matrix_df = load_pickle(root+GENOMIC_MATRIX_PATH)

    if not os.path.exists(root+GENE_EXPRESSION_PATH) and not os.path.exists(root+ANTIBODY_CAPTURE_PATH):
        split_antibody_and_gene(genomic_matrix_df, root)
        
    gene_expression_df = load_pickle(root+GENE_EXPRESSION_PATH)
    antibody_capture_df = load_pickle(root+ANTIBODY_CAPTURE_PATH)
    
    return genomic_matrix_df, gene_expression_df, antibody_capture_df

def load_GSE239626():
    """
    Load data from GSE239626 dataset

    Returns:
        genomic_matrix_df (pd.DataFrame): Genomic matrix data
        gene_expression_df (pd.DataFrame): Gene expression data, subset of genomic matrix
        antibody_capture_df (pd.DataFrame): Antibody capture data, subset of genomic matrix
        family_phenotype_df (pd.DataFrame): Family phenotype data
    """
    if REPOSITORY_PATH in os.getcwd(): root = REPOSITORY_PATH
    else: root = ''
    
    genomic_matrix_df, gene_expression_df, antibody_capture_df = load_genomic_matrix(root)

    if not os.path.exists(root+FAMILY_PATH):
        unzip_file(root+FAMILY_ZIP_PATH)
    family_phenotype_df = pd.read_pickle(root+FAMILY_PATH)

    return genomic_matrix_df, gene_expression_df, antibody_capture_df, family_phenotype_df