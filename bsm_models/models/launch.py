"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contain the function to looking for the bests models for each day and sector.

"""
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from sklearn.externals import joblib
from .basic import get_basic_models
from .advanced import get_advanced_models
from .ensemble import get_ensemble_models
from utilities.processing import get_non_n_cols, get_unwanted_cols
from classification.categorize import split_df_train_test_by_date


def make_magic(df_, days_, mode_debug=True):
    """
    This function split the data into train and test and calculate various models to choose the best one
    for each day and sector and finally save the bests models.

    :param pd.DataFrame df_: Dataframe with procesed info.
    :param list days_: List with the days of the columns.
    :param bool mode_debug: Boolean to choose if create models with all data in train or with only a year.
    """
    df_train, df_test = split_df_train_test_by_date(df_, 2019, mode_debug)
    for sector in df_['sector_gics'].unique():
        df_train_sct = df_train[df_train['sector_gics'] == sector]
        df_test_sct = df_test[df_test['sector_gics'] == sector]
        for day_ in days_:
            path_to_save = '../models/%s/%i' % (sector, day_)
            if not os.path.isdir(os.path.abspath(path_to_save)):
                os.makedirs(os.path.abspath(path_to_save))

            list_to_drop = get_non_n_cols(df_train_sct, int(day_))
            df_train_sct_non_n = df_train_sct.drop(list_to_drop, axis='columns')
            df_test_sct_non_n = df_test_sct.drop(list_to_drop, axis='columns')

            target_train = df_train_sct_non_n['cat_close_shifted_%d' % day_]
            feat_train = df_train_sct_non_n[df_train_sct_non_n.select_dtypes(float).columns]

            target_test = df_test_sct_non_n['cat_close_shifted_%d' % day_]
            feat_test = df_test_sct_non_n[df_test_sct_non_n.select_dtypes(float).columns]

            list_to_drop_2 = get_unwanted_cols(feat_train)

            feat_train = feat_train.drop(list_to_drop_2, axis='columns')
            feat_test = feat_test.drop(list_to_drop_2, axis='columns')
            dict_basic, dict_log_reg, dict_knn, dict_dec_tree = get_basic_models(feat_train.values, target_train.values,
                                                                                 feat_test.values, target_test.values,
                                                                                 day_, sector)

            best_models = [dict_log_reg['log_reg'][0], dict_knn['knn'][0], dict_dec_tree['dec_tree'][0]]

            dict_ensem, dict_vot, dict_bagg, dict_ada = get_ensemble_models(feat_train.values, target_train.values,
                                                                            feat_test.values,
                                                                            target_test.values, day_, sector,
                                                                            best_models)
            dict_advan, dict_rand_for, dict_light = get_advanced_models(feat_train.values, target_train.values,
                                                                        feat_test.values, target_test.values, day_,
                                                                        sector)
            best_basic = list(dict_basic['best'].keys())
            best_ensem = list(dict_ensem['best'].keys())
            best_advan = list(dict_advan['best'].keys())

            prec_basic = float(dict_basic['best'][best_basic[0]][3]['weighted avg']['precision'])
            prec_ensem = float(dict_ensem['best'][best_ensem[0]][2]['weighted avg']['precision'])
            prec_advan = float(dict_advan['best'][best_advan[0]][3]['weighted avg']['precision'])

            if prec_basic >= prec_ensem:
                if prec_basic >= prec_advan:
                    model_name = '/%s.mdl' % best_basic[0]
                    joblib.dump(dict_basic['best'][best_basic[0]][1], path_to_save + model_name.replace(' ', '_'))
                    best_params = pd.DataFrame(index=dict_basic['best'][best_basic[0]][0].keys(),
                                               data=list(dict_basic['best'][best_basic[0]][0].values()),
                                               columns=['best_values'])
                    report = pd.DataFrame(dict_basic['best'][best_basic[0]][3])
                    with pd.ExcelWriter(path_to_save + '/report_%s.xlsx' % best_basic[0]) as wrt:
                        best_params.to_excel(wrt, sheet_name='best_params')
                        report.to_excel(wrt, sheet_name='report')
                else:
                    model_name = '/%s.mdl' % best_advan[0]
                    joblib.dump(dict_advan['best'][best_advan[0]][1], path_to_save + model_name.replace(' ', '_'))
                    best_params = pd.DataFrame(index=dict_advan['best'][best_advan[0]][0].keys(),
                                               data=list(dict_advan['best'][best_advan[0]][0].values()),
                                               columns=['best_values'])
                    report = pd.DataFrame(dict_advan['best'][best_advan[0]][3])
                    with pd.ExcelWriter(path_to_save + '/report_%s.xlsx' % best_advan[0]) as wrt:
                        best_params.to_excel(wrt, sheet_name='best_params')
                        report.to_excel(wrt, sheet_name='report')
            else:
                if prec_ensem >= prec_advan:
                    model_name = '/%s.mdl' % best_ensem[0]
                    joblib.dump(dict_ensem['best'][best_ensem[0]][1], path_to_save + model_name.replace(' ', '_'))
                    report = pd.DataFrame(dict_ensem['best'][best_ensem[0]][2])
                    with pd.ExcelWriter(path_to_save + '/report_%s.xlsx' % best_ensem[0]) as wrt:
                        report.to_excel(wrt, sheet_name='report')
                else:
                    model_name = '/%s.mdl' % best_advan[0]
                    joblib.dump(dict_advan['best'][best_advan[0]][1], path_to_save + model_name.replace(' ', '_'))
                    best_params = pd.DataFrame(index=dict_advan['best'][best_advan[0]][0].keys(),
                                               data=list(dict_advan['best'][best_advan[0]][0].values()),
                                               columns=['best_values'])
                    report = pd.DataFrame(dict_advan['best'][best_advan[0]][3])
                    with pd.ExcelWriter(path_to_save + '/report_%s.xlsx' % best_advan[0]) as wrt:
                        best_params.to_excel(wrt, sheet_name='best_params')
                        report.to_excel(wrt, sheet_name='report')
