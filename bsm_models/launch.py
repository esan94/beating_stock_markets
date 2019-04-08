"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script is the launch to create models.

"""

import pandas as pd
import numpy as np

from models.launch import make_magic
from classification.categorize import categorize_each_difference
from utilities.processing import interpolate_nan_values, add_shifts


def load_and_transform():
    """
    Load and transform categorical and financial data to use in models.

    :return pd.DataFrame: Dataframe to use in models.
    """
    df_categorical = pd.read_csv('../data/db_bsm_categorical.csv')
    df_financial = pd.read_csv('../data/db_bsm_financial.csv')
    df_financial.replace(0, np.NaN, inplace=True)
    df_financial_not_nan = interpolate_nan_values(df_financial, ['close', 'volume'])
    df_financial_not_nan = df_financial_not_nan.sort_values(['ticker', 'date'], ascending=[True, False])
    for num_ in [3, 5, 7, 14, 21]:
        df_financial_not_nan = add_shifts(df_financial_not_nan, 'close', 'close_shifted_%i' % num_, num_)
    df_financial_not_nan.dropna(subset=['close_shifted_21'], inplace=True)
    df_fin_not_nan = interpolate_nan_values(df_financial_not_nan, list(df_financial_not_nan.select_dtypes(float)))
    df_fin_not_nan['date'] = pd.to_datetime(df_fin_not_nan['date'])
    df_final = categorize_each_difference([3, 5, 7, 14, 21], df_fin_not_nan)
    df_categorical = df_categorical.dropna()
    df_categorical = df_categorical.drop_duplicates(subset=['ticker'], keep='first')
    df_final = pd.merge(left=df_final, right=df_categorical, how='inner', on='ticker')
    df_final = df_final.dropna()
    return df_final


def create_models():
    """
    Main function that load and transform data for calculate the bests models.
    """
    df_procesed = load_and_transform()
    make_magic(df_procesed, [3, 5, 7, 14, 21])


if __name__ == '__main__':
    create_models()
