"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains functions to use as a convenience.

"""

import re
import pandas as pd


def add_shifts(df_, col_to_shift, new_col, shift):
    """
    This function add shifted columns to data by ticker.

    :param pd.DataFrame df_: Dataframe with financial data.
    :param str col_to_shift: Column over to create the shift.
    :param str new_col: Name of the shifted column.
    :param int shift: Days to use as shift.
    :return pd.DataFrame: Dataframe with the shift added.
    """

    for id_ in df_['ticker'].unique():
        df_by_id = df_[df_['ticker'] == id_]
        df_.loc[df_['ticker'] == id_, new_col] = - df_by_id[col_to_shift] + df_by_id[col_to_shift].shift(shift) # Change sign

    return df_


def get_non_n_cols(df_, n):
    """
    Get the columns that his time window is less than n days.

    :param pd.DataFrame df_: Dataframe with financial data.
    :param int n: n days to get columns with.
    :return list: List with the name of the columns.
    """

    return [elem for elem in df_.columns if
            (re.search(r'\d+$', elem) is not None) and (int(elem[-2:].strip().strip('_')) < n)]


def get_unwanted_cols(df_):
    """
    This functions gives columns to drop from df_.

    :param pd.DataFrame df_: Dataframe to calc unwanted columns.
    :return list: Name of the unwanted columns from df_.
    """
    return [elem for elem in df_.columns if
            elem.startswith('close_shifted') or
            elem.startswith('cat_close_shifted')]


def interpolate_nan_values(df_, to_interpolate):
    """
    Interpolate and extrapolate nan values for numerical columns.

    :param pd.DataFrame df_: Dataframe with financial data with NaN values.
    :param list to_interpolate: List with columns to interpolate.
    :return pd.DataFrame: Dataframe with financial data without NaN values.
    """

    list_df = []
    for tick in df_['ticker'].unique():
        df_by_ticker = df_[df_['ticker'] == tick]
        for col in to_interpolate:
            df_by_ticker[col] = df_by_ticker[col].interpolate(method='linear', limit_direction='both')
        list_df.append(df_by_ticker)
    return pd.concat(list_df)
