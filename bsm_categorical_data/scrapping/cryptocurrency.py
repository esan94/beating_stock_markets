"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains a function to bring information about cryptos
from https://finance.yahoo.com.

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_cryptocurrency_from_yahoo_finance():
    """
    This function bring information about cryptocurrency.

    :return pd.DataFrame: Dataframe with info about cryptos.
    """

    url_ = 'https://finance.yahoo.com/cryptocurrencies'
    html_ = requests.get(url_)
    soup_ = BeautifulSoup(html_.content, 'html.parser')
    num_of_ind = int(soup_.findAll('div', class_='D(ib)')[2].get_text().split(' ')[3])
    limit = int(str(int(num_of_ind / 100) + 1) + '00')
    _ = 0
    df_list = []
    while _ < limit:
        listing = []
        url_data = url_ + '?offset=%s&count=100'
        html_ = requests.get(url_data % _)
        soup_ = BeautifulSoup(html_.content, 'html.parser')
        tags = soup_.findAll('a', class_="Fw(b)")
        for __ in range(len(tags)):
            if tags[__].get_text() != 'All Screeners':
                features = [tags[__].get_text(),
                            str(tags[__])[0:-8].split('title=')[-1].split('"')[1]]
                listing.append(features)
        _ += 100
        df_cryp = pd.DataFrame(data=listing, columns=['ticker', 'company'])
        df_cryp['sector'] = 'Cryptocurrency'
        df_cryp['language'] = 'crypto'
        df_list.append(df_cryp)

    return pd.concat(df_list, ignore_index=True)
