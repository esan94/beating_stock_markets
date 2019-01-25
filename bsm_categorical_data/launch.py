"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This is the main script for launching the program. The script calls functions
in package scrapping to bring all required categorical data from yahoo finance
then, data have to be processing to make a final bbdd of categorical data.

"""
import os
from time import time

import pandas as pd
import numpy as np

from scrapping.sectors import get_industries_by_sector_from_yahoo_finance_com as get_sectors_com
from scrapping.sectors import get_industries_by_sector_from_yahoo_finance as get_sectors_cntr
from scrapping.cryptocurrency import get_cryptocurrency_from_yahoo_finance as get_crypto
from scrapping.index import get_industries_by_index_from_yahoo_finance as get_index
from scrapping.country import get_country_by_ticker
from scrapping.country import save_well_ticker_without_country as save_without_country
from processing.data import yahoo_sector_to_sector_gics as sector_gics
from processing.data import yahoo_sector_to_sector_icb as sector_icb
from processing.data import change_country_which_contains as change_country
from utilities.time import show_time
import utilities.constants as ctes


def process_country(df_db_country):
    """
    This function process the country column of a dataframe and as last part write
    in csv the results.

    :param pd.DataFrame df_db_country: Dataframe with information about countries and
    companies.
    """

    print('Initializing process country')
    t_init = time()
    df_db_country['country'] = df_db_country['country'].replace(np.nan, 'nan')
    country_list = ctes.LIST_COUNTRIES
    for cntr in country_list:
        df_db_country['country'] = df_db_country['country'].apply(change_country,
                                                                  args=(cntr,))

    df_db_country.loc[df_db_country['country'].str.contains('States'),
                      'country'] = 'United States'
    df_db_country.loc[df_db_country['country'].str.contains('Kong'),
                      'country'] = 'Hong Kong'
    df_db_country.loc[df_db_country['country'].str.contains('Island'),
                      'country'] = 'Cayman Islands'
    df_db_country.loc[df_db_country['ticker'] == 'WAAS',
                      'country'] = 'British Virgin Islands'

    df_db_country = df_db_country.drop(labels=['language', 'sector'], axis=1)
    df_db_country = df_db_country[~df_db_country.duplicated(keep='first')]

    dir_ = os.path.realpath(os.path.join(os.getcwd(), '..', 'data'))
    if not os.path.isdir(dir_):
        os.mkdir(dir_)
    path_ = os.path.join(dir_, 'db_bsm_categorical.csv')
    df_db_country.to_csv(path_, sep=',', index=False)
    show_time(t_init, time(), 'End of process country in time')


def get_country(df_db, is_debug_mode):
    """
    This function bring information about the country of the companies.

    :param pd.DataFrame df_db: Database dataframe with tickets.
    :param bool is_debug_mode: If this boolean is True then write into csv middle dataframes
    otherwise only write into csv final dataframe.
    """

    print('Initializing get country')
    t_init = time()
    df_aux = df_db[~df_db['ticker'].duplicated()]['ticker'].to_frame()
    df_aux['country'] = get_country_by_ticker(df_aux['ticker'])
    if is_debug_mode:
        dir_ = os.path.realpath(os.path.join(os.getcwd(), '..', 'data'))
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        df_aux.to_csv(os.path.join(dir_, 'debug_yahoo_ticker_by_country.csv'), index=False)
    list_to_save = [save_without_country(tick)
                    for tick in df_aux[df_aux['country'] == 'None']['ticker'].unique()]
    list_to_save = [elem for elem in list_to_save if elem is not None]
    list_to_save.extend(df_aux[df_aux['country'] != 'None']['ticker'].unique())
    df_aux = df_aux[df_aux['ticker'].isin(list_to_save)]
    df_db_country = pd.merge(left=df_db, right=df_aux, how='left', on=['ticker'])
    show_time(t_init, time(), 'End of get country in time')
    process_country(df_db_country)


def make_db_with_index(df_sector, is_debug_mode):
    """
    This function is to make a db with stock index.

    :param pd.DataFrame df_sector: Dataframe with processing sectors.
    :param bool is_debug_mode: If this boolean is True then write into csv middle dataframes
    otherwise only write into csv final dataframe.
    :return pd.DataFrame: Dataframe with info about stock index.
    """

    print('Initializing data base with index')
    t_init = time()
    df_index = get_index(ctes.INDEXES)
    if is_debug_mode:
        dir_ = os.path.realpath(os.path.join(os.getcwd(), '..', 'data'))
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        df_index.to_csv(os.path.join(dir_, 'debug_yahoo_index.csv'),
                        index=False)

    df_db = pd.merge(left=df_sector, right=df_index, how='outer',
                     on=['ticker', 'company'])
    show_time(t_init, time(), 'End of making database with index in time')
    return df_db


def process_sectors(df_sector, is_debug_mode):
    """
    This function if to process sector data in a dataframe into gics and icb.

    :param pd.DataFrame df_sector: Dataframe with all ticker by sectors.
    :param bool is_debug_mode: If this boolean is True then write into csv middle dataframes
    otherwise only write into csv final dataframe.
    :return pd.DataFrame: Dataframe with processing sectors.
    """

    print('Initializing processing sectors')
    t_init = time()
    list_sctr_gics = [ctes.LIST_GICS_COM_SERV, ctes.LIST_GICS_CONS_DISC, ctes.LIST_GICS_CONS_STP,
                      ctes.LIST_GICS_ENERGY, ctes.LIST_GICS_FINANCIAL, ctes.LIST_GICS_HEALTH,
                      ctes.LIST_GICS_REAL_STATE, ctes.LIST_GICS_INDUSTRIALS,
                      ctes.LIST_GICS_INF_TECH, ctes.LIST_GICS_UTILITIES]
    list_sctr_icb = [ctes.LIST_ICB_OIL_GAS, ctes.LIST_ICB_BASIC_MAT, ctes.LIST_ICB_INDUSTRIALS,
                     ctes.LIST_ICB_CONS_GOOD, ctes.LIST_ICB_HEALTH, ctes.LIST_ICB_TECH,
                     ctes.LIST_ICB_FINANCIAL, ctes.LIST_ICB_UTILITIES, ctes.LIST_ICB_TELECOM,
                     ctes.LIST_ICB_CONS_SERV]
    for value_gics, key_gics in zip(list_sctr_gics, ctes.LIST_GICS_NAMES):
        df_sector = sector_gics(df_=df_sector, yahoo_list=value_gics, sector_gics=key_gics)

    for value_icb, key_icb in zip(list_sctr_icb, ctes.LIST_ICB_NAMES):
        df_sector = sector_icb(df_=df_sector, yahoo_list=value_icb, sector_icb=key_icb)

    df_sector.loc[df_sector['sector'] == 'Cryptocurrency', 'sector_gics'] = 'Cryptocurrency'
    df_sector.loc[df_sector['sector'] == 'Cryptocurrency', 'sector_icb'] = 'Cryptocurrency'

    if is_debug_mode:
        dir_ = os.path.realpath(os.path.join(os.getcwd(), '..', 'data'))
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        df_sector.to_csv(os.path.join(dir_, 'debug_yahoo_sector_processed.csv'), index=False)

    show_time(t_init, time(), 'End of processing sectors in time')
    return df_sector


def get_sectors(is_debug_mode):
    """
    This function is for getting all the info about sectors.

    :param bool is_debug_mode: If this boolean is True then write into csv middle dataframes
    otherwise only write into csv final dataframe.
    :return pd.DataFrame: Dataframe with all ticker by sectors.
    """

    print('Initializing sectors and cryptos')
    t_init = time()

    df_yahoo_com = get_sectors_com(sector_list=ctes.LIST_COM_SECTORS)
    sector_list = [ctes.LIST_ES_SECTORS, ctes.LIST_FR_SECTORS, ctes.LIST_DE_SECTORS,
                   ctes.LIST_IT_SECTORS, ctes.LIST_UK_SECTORS]
    list_df_yahoo_cntr = [get_sectors_cntr(sector_list=sct, lan_=ctes.LIST_LANGUAGES[_])
                          for _, sct in enumerate(sector_list)]
    df_yahoo_cntr = pd.concat(objs=list_df_yahoo_cntr)
    df_crypto = get_crypto()

    if is_debug_mode:
        dir_ = os.path.realpath(os.path.join(os.getcwd(), '..', 'data'))
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        df_yahoo_cntr.to_csv(os.path.join(dir_, 'debug_yahoo_sector_by_country.csv'),
                             index=False)
        df_yahoo_com.to_csv(os.path.join(dir_, 'debug_yahoo_sector.csv'),
                            index=False)
        df_crypto.to_csv(os.path.join(dir_, 'debug_yahoo_crypto.csv'),
                         index=False)

    df_sector = pd.concat(objs=[df_yahoo_com, df_yahoo_cntr, df_crypto])
    show_time(t_init, time(), 'End of sectors and cryptos in time')
    df_sector = process_sectors(df_sector=df_sector, is_debug_mode=is_debug_mode)
    return df_sector


if __name__ == '__main__':
    IS_DEBUG_MODE = False
    DF_SECTORS = get_sectors(IS_DEBUG_MODE)
    DF_DB = make_db_with_index(DF_SECTORS, IS_DEBUG_MODE)
    get_country(DF_DB, IS_DEBUG_MODE)
