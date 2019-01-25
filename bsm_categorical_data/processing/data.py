"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains functions to processing data in dataframes.

"""
import pandas as pd


def yahoo_sector_to_sector_gics(df_, yahoo_list, sector_gics):
    """
    This function change the sector in column yahoo_sector by gics standard at top level
    https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard

    :param pd.DataFrame df_: Dataframe with the column to change.
    :param list yahoo_list: List of the sectors to change.
    :param str sector_gics: List of new sectors.
    :return pd.DataFrame: Dataframe with new classification.
    """

    for y_sector in yahoo_list:
        df_.loc[df_['sector'] == y_sector, 'sector_gics'] = sector_gics
    return df_


def yahoo_sector_to_sector_icb(df_, yahoo_list, sector_icb):
    """
    This function change the sector in column yahoo_sector by icb standard at top level
    https://en.wikipedia.org/wiki/Industry_Classification_Benchmark

    :param pd.DataFrame df_: Dataframe with the column to change.
    :param list yahoo_list: List of the sectors to change.
    :param str sector_icb: List of new sectors.
    :return pd.DataFrame: Dataframe with new classification.
    """

    for y_sector in yahoo_list:
        df_.loc[df_['sector'] == y_sector, 'sector_icb'] = sector_icb
    return df_


def change_country_which_contains(elem, regex):
    """
    This function is to check if a regex is in a string.

    :param str elem: Element of a dataframe.
    :param str regex: Expression to check.
    :return str: Either elem or regex depending on the boolean.
    """

    if regex in elem:
        ret_ = regex
    else:
        ret_ = elem
    return ret_
