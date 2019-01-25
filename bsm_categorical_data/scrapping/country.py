"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains functions which bring info about the country
of the companies.

"""
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


@np.vectorize
def get_country_by_ticker(ticker_):
    """
    This function bring information about countries given a ticker. Is a
    vectorize function.

    :param ticker_:
    :return str or float: The country of the company or nan if does not found something
    """
    url_ = 'https://es.finance.yahoo.com/quote/%s/profile?p=%s' % (ticker_, ticker_)
    html_ = requests.get(url_)
    soup_ = BeautifulSoup(html_.content, 'html.parser')
    txt_ = soup_.findAll('p', class_='D(ib)')
    if len(txt_) == 0:
        ret_ = None
    else:
        text_ = txt_[0].get_text()
        if text_ == '':
            ret_ = None
        else:
            ret_ = ''.join([i for i in text_ if not i.isdigit()]).split('http')[0].split()[-1]
    return ret_


def save_well_ticker_without_country(ticker_):
    """
    This function check if a company without country exists in yahoo finance.

    :param str ticker_: Ticket of a company.
    :return str: Ticket of an existing company-
    """
    url_ = 'https://es.finance.yahoo.com/quote/%s/profile?p=%s' % (ticker_, ticker_)
    html_ = requests.get(url_)
    soup_ = BeautifulSoup(html_.content, 'html.parser')
    title_ = soup_.findAll('html')[0].find('title')
    if ticker_ in title_.get_text():
        ret_ = ticker_
    else:
        ret_ = None
    return ret_
