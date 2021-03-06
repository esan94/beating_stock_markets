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
import time
import random

from models.launch import make_magic
from classification.categorize import categorize_each_difference
from utilities.processing import interpolate_nan_values, add_shifts
from utilities.time import show_time


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
    df_final.replace(0, np.NaN, inplace=True)
    df_final[df_final.select_dtypes(float).columns] = df_final.select_dtypes(float).astype('float32')
    df_final.replace([np.inf, -np.inf], np.NaN, inplace=True)
    df_final = df_final.dropna()
    df_final[df_final.select_dtypes('float32').columns] = df_final.select_dtypes('float32').astype(float)
    return df_final


def create_models():
    """
    Main function that load and transform data for calculate the bests models.
    """
    t_init = time.time()
    df_procesed = load_and_transform()
    show_time(t_init, time.time(), 'Time of previous process ended')
    list_sector = list(df_procesed['sector_gics'].unique())
    make_magic(df_procesed, [3, 5, 7, 14, 21], list_sector, True)
    show_time(t_init, time.time(), 'Time of magic ended')
    make_magic(df_procesed, [3, 5, 7, 14, 21], list_sector, False)
    show_time(t_init, time.time(), 'END')


if __name__ == '__main__':
    create_models()
