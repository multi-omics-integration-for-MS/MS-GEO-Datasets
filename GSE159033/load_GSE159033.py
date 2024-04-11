from utils import unzip_and_extract_file

MATRIX_ZIP_PATH = 'GSE159033\GSE159033_genomic_matrix_matrix.zip'
MATRIX_PATH = 'GSE159033\GSE159033_genomic_matrix_matrix.csv'

FAMILY_ZIP_PATH = 'GSE159033\GSE159033_family_phenotype_data.zip'
FAMILY_PATH = 'GSE159033\GSE159033_family_phenotype_data.csv'


def load_GSE159033():
    genomic_matrix_df = unzip_and_extract_file(MATRIX_ZIP_PATH, MATRIX_PATH)
    family_phenotype_df = unzip_and_extract_file(FAMILY_ZIP_PATH, FAMILY_PATH)

    return genomic_matrix_df, family_phenotype_df