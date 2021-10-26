import ast

import pandas as pd

RESULT_FILE = 'results.csv'


def read_results(path: str):
    df = pd.read_csv(path, index_col=0,
                     converters={'keyphrases': ast.literal_eval},
                     encoding='utf-8-sig')
    return df


DF_RESULTS = read_results(RESULT_FILE)


def keyphrases(name: str):
    return DF_RESULTS.loc[name]['keyphrases']
