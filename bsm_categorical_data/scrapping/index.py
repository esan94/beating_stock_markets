"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains a function to bring information about industries
by index from https://finance.yahoo.com

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_industries_by_index_from_yahoo_finance(index_):
    """
    This function bring info about 30 companies and their index.

    :param dict index_: Dictionary where keys are index in a yahoo way and
    values are their common name for example IBEX 35 or DJI.
    :return pd.DataFrame: Dataframe with info about industries and if they are
    in the index.
    """

    df_list = []
    for key in index_.keys():
        url_ = 'https://finance.yahoo.com/quote/%s/components?p=%s'
        html_ = requests.get(url_ % (key, key))
        soup_ = BeautifulSoup(html_.content, 'html.parser')
        find_all = soup_.findAll('td', class_='Py(10px) Ta(start) Pend(10px)')
        tot_ = len(find_all)
        _ = 0
        feature_list = []
        while _ < tot_:
            feat = [find_all[_].get_text(), find_all[_ + 1].get_text()]
            _ += 2
            feature_list.append(feat)
        df_ = pd.DataFrame(data=feature_list, columns=['ticker', 'company'])
        df_['stock_index'] = index_.get(key)
        df_list.append(df_)

    return pd.concat(objs=df_list)
