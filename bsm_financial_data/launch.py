import os

import pandas as pd
import numpy as np
from configparser import ConfigParser

from alpha_van import alpha_van


def get_data(inputs_, is_premium):
    """

    :param dict inputs_:
    :return:
    """
    key = inputs_.get('key')

    ticker_list = inputs_.get('list')

    list_ticker_by_key = []
    for ticker in ticker_list:
        list_ticker_by_key.extend(alpha_van.get_financials(key, ticker, is_premium))

    return list_ticker_by_key


def main(is_premium):

    path_categorical_df = os.path.join(os.path.join('..', 'data'), 'db_bsm_categorical.csv')
    df_categorical = pd.read_csv(path_categorical_df)
    df_categorical = df_categorical.dropna()
    all_tickers = df_categorical['ticker'].unique()
    config_parser = ConfigParser()
    config_parser.read('config.properties')
    r_list = np.random.randint(0, len(all_tickers), size=4)
    print(r_list)

    inputs_list = [
        {'key': str(config_parser.get('ALPHA_VANTAGE', 'free_key')),
         'list': [all_tickers[rand] for rand in r_list]},

        {'key': str(config_parser.get('ALPHA_VANTAGE', 'premium_key')),
         'list': all_tickers}
    ]

    if is_premium:
        f_list = get_data(inputs_list[1], is_premium)
    else:
        f_list = get_data(inputs_list[0], is_premium)

    path_financial_df = os.path.join(os.path.join('..', 'data'), 'db_bsm_financial.csv')
    df_financial = pd.concat(f_list)
    df_financial.to_csv(path_financial_df, index=False)


if __name__ == '__main__':
    IS_PREMIUM = False
    main(IS_PREMIUM)
