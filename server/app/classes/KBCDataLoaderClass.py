import pandas as pd


class KBCDataLoaderClass:

    def __init__(self):
        None


    def load_pandas_csv(self, file_path, header=None):
        return pd.read_csv(file_path, header=header)

    def load_pandas_txt(self, file_path, header=None, sep='\t'):
        return pd.read_csv(file_path, header=header, sep=sep)