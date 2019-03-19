"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This is the main script to launching the program. The script calls functions
in package alpha_van to bring financial data from alpha_vantage. There are two
ways, with a free account or a premium one. With the premium you only can have
four randomly companies.

"""
import os
import time

import pandas as pd
import numpy as np
from configparser import ConfigParser

from alpha_van import alpha_van
from utilities.times import show_time


def get_data(inputs_, is_premium):
    """
    Function to get data from the api.

    :param dict inputs_: Dictionary with info about user key and tickers
    :param bool is_premium: Boolean wich decide if the key to choose is
    for free account or for premium account.
    :return list: List with all data requested.
    """

    key = inputs_.get('key')

    ticker_list = inputs_.get('list')

    list_ticker_by_key = []
    for ticker in ticker_list:
        list_ticker_by_key.extend(alpha_van.get_financials(key, ticker, is_premium))

    return list_ticker_by_key


def main(is_premium):
    """
    Principal function of the script.

    :param bool is_premium: Boolean wich decide if the key to choose is
    for free account or for premium account.
    """

    path_categorical_df = os.path.join(os.path.join('..', 'data'), 'db_bsm_categorical.csv')
    df_categorical = pd.read_csv(path_categorical_df)
    df_categorical = df_categorical.dropna()
    all_tickers = df_categorical['ticker'].unique()
    config_parser = ConfigParser()
    config_parser.read('config.properties')
    r_list = np.random.randint(0, len(all_tickers), size=4)
    f_list = []

    inputs_list = [
        {'key': str(config_parser.get('ALPHA_VANTAGE', 'free_key')),
         'list': [all_tickers[rand] for rand in r_list]},

        {'key': str(config_parser.get('ALPHA_VANTAGE', 'premium_key')),
         'list': all_tickers}
    ]
    try:
        if is_premium:
            f_list.extend(get_data(inputs_list[1], is_premium))
        else:
            f_list.extend(get_data(inputs_list[0], is_premium))
    except KeyError:
        all_ticker_saved = [tick.split('.')[0] for tick in os.listdir(os.path.join('..', 'data'))]
        all_tickers = list(set(all_tickers) - set(all_ticker_saved))
        inputs_list = [
            {'key': str(config_parser.get('ALPHA_VANTAGE', 'premium_key')),
             'list': all_tickers}
        ]
        if is_premium:
            f_list.extend(get_data(inputs_list[0], is_premium))
        else:
            raise ValueError('An api key premium in Alpha Vantage is needed.')

    path_financial_df = os.path.join(os.path.join('..', 'data'), 'db_bsm_financial.csv')
    df_financial = pd.concat(f_list)
    df_financial.to_csv(path_financial_df, index=False)


if __name__ == '__main__':
    IS_PREMIUM = True
    T_INIT = time.time()
    main(IS_PREMIUM)
    show_time(T_INIT, time.time(), 'ALL DATA COLLECTED')
