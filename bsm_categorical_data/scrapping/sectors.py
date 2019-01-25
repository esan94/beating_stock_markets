"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains functions to bring information about sectors, for
tickers in the stock market, from yahoo finance.

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_industries_by_sector_from_yahoo_finance_com(sector_list):
    """
    This function bring information about sectors from yahoo https://finance.yahoo.com

    :param list sector_list: List with the business sectors in the web.
    :return pd.DataFrame: Dataframe with tickers and sectors for the web.
    """

    url = 'https://finance.yahoo.com'
    df_list = []
    for sctr in sector_list:
        url_num_of_ind = url + '/sector/%s' % sctr
        html_ = requests.get(url_num_of_ind)
        soup_ = BeautifulSoup(html_.content, 'html.parser')
        num_of_ind = int(soup_.findAll('div', class_='D(ib)')[2].get_text().split(' ')[3])
        limit = int(str(int(num_of_ind / 100) + 1) + '00')
        _ = 0
        listing = []
        while _ < limit:
            url_extract_data = url + '/screener/predefined/%s?offset=%i&count=%i' % (sctr, _, 100)
            html_ = requests.get(url_extract_data)
            soup_ = BeautifulSoup(html_.content, 'html.parser')
            tags = soup_.findAll('a', class_='Fw(b)')
            for __ in range(len(tags)):
                if tags[__].get_text() != 'All Screeners':
                    features = [tags[__].get_text(),
                                str(tags[__])[0:-8].split('title=')[-1].split('"')[1]]
                    listing.append(features)
            _ += 100
        df_ind_sector = pd.DataFrame(data=listing, columns=['ticker', 'company'])
        df_ind_sector['sector'] = sctr
        df_ind_sector['language'] = 'com'
        df_list.append(df_ind_sector)

    return pd.concat(df_list, ignore_index=True)


def get_industries_by_sector_from_yahoo_finance(sector_list, lan_):
    """
    This function bring information about sectors from yahoo on different
    countries.

    :param list sector_list: List with the business sectors in the web.
    :param str lan_: String with the language of the country for the web,
    these are: es, fr, uk, it, de.
    :return pd.DataFrame: Dataframe with tickers and sectors for the web.
    """

    url = 'https://%s.finance.yahoo.com/industries/%s'
    df_list = []
    for sctr in sector_list:
        listing = []
        html_ = requests.get(url % (lan_, sctr))
        soup_ = BeautifulSoup(html_.content, 'html.parser')
        tags = soup_.findAll('a', class_='Fw(b)')
        for _ in range(len(tags)):
            features = [tags[_].get_text(),
                        str(tags[_])[0:-8].split('title=')[-1].split('"')[1]]
            listing.append(features)
        df_ind_sector = pd.DataFrame(data=listing, columns=['ticker', 'company'])
        df_ind_sector['sector'] = sctr
        df_ind_sector['language'] = lan_
        df_list.append(df_ind_sector)

    return pd.concat(df_list, ignore_index=True)
