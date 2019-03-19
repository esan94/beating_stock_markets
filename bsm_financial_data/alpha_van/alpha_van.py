"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script manages times about the process.

"""
import time
import os

import pandas as pd

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from utilities.times import set_time_sleep as sleep
from utilities.times import show_time


def get_time_series(alpha_key, ticker, is_premium):
    """
    This function bring info from alpha vantage, filter from 2004 and
    take only close and volume columns.

    :param str alpha_key: Key from Alpha Vantage
    :param str ticker: list of tickers to download
    :param bool is_premium: Boolean to chose the key.
    :return pd.DataFrame: Dataframe with close and volume data of ticker
    from ticker_list.
    """
    t_init = time.time()

    ts = TimeSeries(key=alpha_key, output_format='pandas', indexing_type='date')
    sleep(is_premium)
    data_ = ts.get_daily(symbol=ticker, outputsize='full')[0]
    data_['ticker'] = ticker
    data_ = data_.reset_index()
    data_ = data_.drop(labels=['1. open', '2. high', '3. low'], axis=1)
    data_ = data_.rename(columns={'4. close': 'close', '5. volume': 'volume'})
    data_['date'] = pd.to_datetime(data_['date'])
    data_ = data_[data_['date'].dt.year >= 2004]
    show_time(t_init, time.time(), 'Time serie for ticker %s done in time:' % ticker)
    return data_


def get_sma(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring sma data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_sma = ti.get_sma(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_sma.columns = [' '.join([col, period]) for col in data_sma.columns]
        df_by_ticker.append(data_sma)


def get_wma(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring wma data for ticker.
    
    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_wma = ti.get_wma(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_wma.columns = [' '.join([col, period]) for col in data_wma.columns]
        df_by_ticker.append(data_wma)


def get_dema(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring dema data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    for period in time_period_list:
        data_dema = ti.get_dema(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_dema.columns = [' '.join([col, period]) for col in data_dema.columns]
        df_by_ticker.append(data_dema)


def get_kama(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring kama data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_kama = ti.get_kama(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_kama.columns = [' '.join([col, period]) for col in data_kama.columns]
        df_by_ticker.append(data_kama)
    

def get_rsi(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring rsi data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_rsi = ti.get_rsi(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_rsi.columns = [' '.join([col, period]) for col in data_rsi.columns]
        df_by_ticker.append(data_rsi)
    

def get_adx(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring adx data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    for period in time_period_list:
        data_adx = ti.get_adx(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_adx.columns = [' '.join([col, period]) for col in data_adx.columns]
        df_by_ticker.append(data_adx)
    

def get_mom(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring mom data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_mom = ti.get_mom(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_mom.columns = [' '.join([col, period]) for col in data_mom.columns]
        df_by_ticker.append(data_mom)


def get_bop(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring bop data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_bop = ti.get_bop(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_bop.columns = [' '.join([col, period]) for col in data_bop.columns]
        df_by_ticker.append(data_bop)


def get_cci(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring cci data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_cci = ti.get_cci(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_cci.columns = [' '.join([col, period]) for col in data_cci.columns]
        df_by_ticker.append(data_cci)
    

def get_cmo(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring cmo data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_cmo = ti.get_cmo(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_cmo.columns = [' '.join([col, period]) for col in data_cmo.columns]
        df_by_ticker.append(data_cmo)


def get_rocr(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring rocr data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_rocr = ti.get_rocr(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_rocr.columns = [' '.join([col, period]) for col in data_rocr.columns]
        df_by_ticker.append(data_rocr)


def get_aroon(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring aroon data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_aroon = ti.get_aroon(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_aroon.columns = [' '.join([col, period]) for col in data_aroon.columns]
        df_by_ticker.append(data_aroon)


def get_dx(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring dx data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_dx = ti.get_dx(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_dx.columns = [' '.join([col, period]) for col in data_dx.columns]
        df_by_ticker.append(data_dx)
    

def get_minus_di(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring minus_di data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_minus_di = ti.get_minus_di(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_minus_di.columns = [' '.join([col, period]) for col in data_minus_di.columns]
        df_by_ticker.append(data_minus_di)


def get_plus_di(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring plus_di data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_plus_di = ti.get_plus_di(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_plus_di.columns = [' '.join([col, period]) for col in data_plus_di.columns]
        df_by_ticker.append(data_plus_di)


def get_minus_dm(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring minus_dm data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_minus_dm = ti.get_minus_dm(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_minus_dm.columns = [' '.join([col, period]) for col in data_minus_dm.columns]
        df_by_ticker.append(data_minus_dm)
    

def get_plus_dm(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring plus_dm data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_plus_dm = ti.get_plus_dm(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_plus_dm.columns = [' '.join([col, period]) for col in data_plus_dm.columns]
        df_by_ticker.append(data_plus_dm)
    

def get_bbands(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring bbands data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_bbands = ti.get_bbands(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_bbands.columns = [' '.join([col, period]) for col in data_bbands.columns]
        df_by_ticker.append(data_bbands)


def get_natr(ti, ticker, df_by_ticker, time_period_list, is_premium):
    """
    This function bring natr data for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param list df_by_ticker: List where save new data.
    :param list time_period_list: List with the periods of downloading.
    :param bool is_premium: Boolean to chose the key.
    """
    
    for period in time_period_list:
        data_natr = ti.get_natr(symbol=ticker, time_period=int(period))[0]
        sleep(is_premium)
        data_natr.columns = [' '.join([col, period]) for col in data_natr.columns]
        df_by_ticker.append(data_natr)


def get_no_period(ti, ticker, t_init, df_by_ticker, is_premium):
    """
    This function bring data without period for ticker.

    :param alpha_vantage.techindicators.TechIndicator ti: Alpha vantage obj.
    :param str ticker: Ticker of a company.
    :param float t_init: Initial time.
    :param list df_by_ticker: List where save new data.
    :param bool is_premium: Boolean to chose the key.
    """

    data_mama = ti.get_mama(symbol=ticker)[0]
    df_by_ticker.append(data_mama)
    sleep(is_premium)
    show_time(t_init, time.time(), 'MAMA data for ticker %s done in time:' % ticker)

    data_macd = ti.get_macd(symbol=ticker)[0]
    df_by_ticker.append(data_macd)
    sleep(is_premium)
    show_time(t_init, time.time(), 'MACD data for ticker %s done in time:' % ticker)

    data_stoch = ti.get_stoch(symbol=ticker)[0]
    df_by_ticker.append(data_stoch)
    sleep(is_premium)
    show_time(t_init, time.time(), 'STOCH data for ticker %s done in time:' % ticker)

    data_ppo = ti.get_ppo(symbol=ticker)[0]
    df_by_ticker.append(data_ppo)
    sleep(is_premium)
    show_time(t_init, time.time(), 'PPO data for ticker %s done in time:' % ticker)

    data_ultsoc = ti.get_ultsoc(symbol=ticker)[0]
    df_by_ticker.append(data_ultsoc)
    sleep(is_premium)
    show_time(t_init, time.time(), 'ULTSOC data for ticker %s done in time:' % ticker)

    data_sare = ti.get_sar(symbol=ticker)[0]
    df_by_ticker.append(data_sare)
    sleep(is_premium)
    show_time(t_init, time.time(), 'SAR data for ticker %s done in time:' % ticker)

    data_ad = ti.get_ad(symbol=ticker)[0]
    df_by_ticker.append(data_ad)
    sleep(is_premium)
    show_time(t_init, time.time(), 'AD data for ticker %s done in time:' % ticker)

    data_obv = ti.get_obv(symbol=ticker)[0]
    df_by_ticker.append(data_obv)
    sleep(is_premium)
    show_time(t_init, time.time(), 'OBV data for ticker %s done in time:' % ticker)


def get_technical_indicators(alpha_key, ticker, is_premium):
    """
    This function bring all technical indicators.

    :param str alpha_key: User key of Alpha Vantage website.
    :param str ticker: Ticker of a company.
    :param bool is_premium: Boolean to chose the key.
    """

    ti = TechIndicators(key=alpha_key, output_format='pandas')

    time_period_list = ['3', '5', '7', '14', '21', '42']

    t_init = time.time()
    df_by_ticker = []
    get_sma(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'SMA data for ticker %s done in time:' % ticker)
    get_wma(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'WMA data for ticker %s done in time:' % ticker)
    get_dema(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
             time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'DEMA data for ticker %s done in time:' % ticker)
    get_kama(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
             time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'KAMA data for ticker %s done in time:' % ticker)
    get_rsi(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'RSI data for ticker %s done in time:' % ticker)
    get_adx(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'ADX data for ticker %s done in time:' % ticker)
    get_mom(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'MOM data for ticker %s done in time:' % ticker)
    get_cci(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'CCI data for ticker %s done in time:' % ticker)
    get_bop(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'BOP data for ticker %s done in time:' % ticker)
    get_cmo(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
            time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'CMO data for ticker %s done in time:' % ticker)
    get_rocr(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
             time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'ROCR data for ticker %s done in time:' % ticker)
    get_aroon(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
              time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'AROON data for ticker %s done in time:' % ticker)
    get_dx(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
           time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'DX data for ticker %s done in time:' % ticker)
    get_minus_di(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
                 time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'MINUS DI data for ticker %s done in time:' % ticker)
    get_plus_di(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
                time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'PLUS DI data for ticker %s done in time:' % ticker)
    get_minus_dm(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
                 time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'MINUS DM data for ticker %s done in time:' % ticker)
    get_plus_dm(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
                time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'PLUS DM data for ticker %s done in time:' % ticker)
    get_bbands(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,
               time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'BBANDS data for ticker %s done in time:' % ticker)
    get_natr(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker, 
             time_period_list=time_period_list, is_premium=is_premium)
    show_time(t_init, time.time(), 'NATR data for ticker %s done in time:' % ticker)
    get_no_period(ti=ti, ticker=ticker, df_by_ticker=df_by_ticker,  t_init=t_init, is_premium=is_premium)
    df_ticker = pd.concat(df_by_ticker, axis=1, join='inner')
    df_ticker['ticker'] = ticker
    df_ticker = df_ticker.reset_index()
    df_ticker['date'] = pd.to_datetime(df_ticker['date'])
    df_ticker = df_ticker[df_ticker['date'].dt.year >= 2004]
    show_time(t_init, time.time(), 'ALL Technical data for ticker %s done in time:' % ticker)

    return df_ticker


def get_financials(alpha_key, ticker, is_premium):
    """
    This function bring all financial data.

    :param str alpha_key: User key of Alpha Vantage website.
    :param str ticker: Ticker of a company.
    :param bool is_premium: Boolean to chose the key.
    """

    fin_list = []
    df_ts = get_time_series(alpha_key, ticker, is_premium)
    df_tech = get_technical_indicators(alpha_key, ticker, is_premium)
    df_fin = pd.merge(left=df_ts, right=df_tech, how='inner', on=['date', 'ticker'])
    path_fin_df = os.path.join(os.path.join('..', 'data'), '%s.csv' % ticker)
    df_fin.to_csv(path_fin_df, index=False)

    fin_list.append(df_fin)

    return fin_list



