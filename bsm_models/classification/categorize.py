"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains functions to classify the data.

"""

import pandas as pd


def categorize_each_difference(num_list, df_):
    """
    This function categorize the shifted columns in Weak Bull o Bear (W. Bull, W. Bear),
    Bull or Bear and Strong Bull or Bear (S. Bull, S. Bear) depending on the value of the shifted column and
    his statistics (median, p25, p75) by ticker, year, month and sign.

    :param list num_list: List with days to categorize.
    :param pd.DataFrame df_: Dataframe to categorize.
    :return pd.DataFrame: Dataframe recalculated.
    """
    cols_to_keep = list(df_.columns)
    df_['year'], df_['month'] = df_['date'].dt.year, df_['date'].dt.month
    for num_ in num_list:
        df_.loc[df_['close_shifted_%i' % num_] >= 0, 'sign_%i' % num_] = 'Bull'
        df_.loc[df_['close_shifted_%i' % num_] < 0, 'sign_%i' % num_] = 'Bear'
        group = df_.groupby(['ticker', 'year', 'month', 'sign_%i' % num_])['close_shifted_%i' % num_].describe()
        group = group[['25%', '50%', '75%', 'std']].reset_index()
        group.rename({'std': 'std_%i' % num_}, axis='columns', inplace=True)
        df_ = pd.merge(left=df_, right=group, on=['ticker', 'year', 'month', 'sign_%i' % num_], how='inner')

        df_.loc[(df_['sign_%i' % num_] == 'Bull') &
                (df_['close_shifted_%i' % num_] <= df_['50%']), 'cat_close_shifted_%i' % num_] = 'W. ' + df_[
            'sign_%i' % num_]
        df_.loc[(df_['sign_%i' % num_] == 'Bull') &
                (df_['close_shifted_%i' % num_] > df_['50%']) &
                (df_['close_shifted_%i' % num_] < df_['75%']), 'cat_close_shifted_%i' % num_] = df_['sign_%i' % num_]
        df_.loc[(df_['sign_%i' % num_] == 'Bull') &
                (df_['close_shifted_%i' % num_] >= df_['75%']), 'cat_close_shifted_%i' % num_] = 'S. ' + df_[
            'sign_%i' % num_]
        df_.loc[(df_['sign_%i' % num_] == 'Bear') &
                (df_['close_shifted_%i' % num_] >= df_['50%']), 'cat_close_shifted_%i' % num_] = 'W. ' + df_[
            'sign_%i' % num_]
        df_.loc[(df_['sign_%i' % num_] == 'Bear') &
                (df_['close_shifted_%i' % num_] < df_['50%']) &
                (df_['close_shifted_%i' % num_] > df_['25%']), 'cat_close_shifted_%i' % num_] = df_['sign_%i' % num_]
        df_.loc[(df_['sign_%i' % num_] == 'Bear') &
                (df_['close_shifted_%i' % num_] <= df_['25%']), 'cat_close_shifted_%i' % num_] = 'S. ' + df_[
            'sign_%i' % num_]

        df_.drop(['25%', '50%', '75%', 'std_%i' % num_], axis='columns', inplace=True)
        cols_to_keep.extend(['cat_close_shifted_%i' % num_])
    return df_[cols_to_keep]


def add_bull_bear_cat(df_, num_days):
    """
    Creates a new categorical column which has binary info of Bull and Bear.

    :param pd.DataFrame df_: Dataframe to categorize.
    :param list num_days: List of days to categorize.
    :return pd.DataFrame: Recategorized dataframe.
    """
    for day_ in num_days:
        df_.loc[df_['cat_close_shifted_%d' % day_].str.endswith('Bull'), 'cat_%d' % day_] = 'Bull'
        df_.loc[df_['cat_close_shifted_%d' % day_].str.endswith('Bear'), 'cat_%d' % day_] = 'Bear'
    return df_


def split_df_train_test_by_date(df_, year_, mode_debug=True):
    """
    This function separe the df_ in test and train by year and month

    :param pd.DataFrame df_: Dataframe to split.
    :param int year_: Year to use as split.
    :param bool mode_debug: Choose if return a df_train shorter.
    :return tuple: Tuple which contains both df's (train, test).
    """

    df_train = df_[(df_['date'].dt.year < year_)]
    if mode_debug:
        df_train = df_train[df_train['date'].dt.year > year_ - 7]
    df_test = df_[(df_['date'].dt.year >= year_)]
    return df_train, df_test
