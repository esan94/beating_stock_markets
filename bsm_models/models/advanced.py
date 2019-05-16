"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains advanced models to train.

"""
from utilities.utils import get_best_params_from_excel

import time

from utilities.time import show_time
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.utils import parallel_backend
import lightgbm as lgb


def lightgboost(best_params, X_train, y_train, X_test, y_test, scoring, dict_light):
    """
    Function to construct a gradient boosting

    :param dict best_params: A dictionary with the best params of the model.
    :param np.Array X_train: Features train data.
    :param np.Array y_train: Target train data.
    :param np.Array X_test: Features test data.
    :param np.Array y_test: Target test data.
    :param str scoring: Scoring to improve.
    :param dict dict_light: Dictionary for gradient boosting output.
    :return tuple: A tuple with a dict of returns and the precision obtained.
    """
    best_params['num_leaves'] = int(best_params['num_leaves'])
    best_params['max_depth'] = int(best_params['max_depth'])
    light = lgb.LGBMClassifier(**best_params)
    val_score_light = cross_val_score(light, X_train, y_train, cv=3, scoring=scoring).mean()
    light.fit(X_train, y_train)
    report = classification_report(y_test, light.predict(X_test), digits=4, output_dict=True)
    dict_light['light'] = [best_params, light, val_score_light, report]
    prec_light = float(dict_light['light'][3]['weighted avg']['precision'])

    return dict_light, prec_light


def random_forest(best_params, X_train, y_train, X_test, y_test, scoring, dict_rand_for):
    """
    Function to construct a random_forest

    :param dict best_params: A dictionary with the best params of the model.
    :param np.Array X_train: Features train data.
    :param np.Array y_train: Target train data.
    :param np.Array X_test: Features test data.
    :param np.Array y_test: Target test data.
    :param str scoring: Scoring to improve.
    :param dict dict_rand_for: Dictionary for random forest output.
    :return tuple: A tuple with a dict of returns and the precision obtained.
    """
    rand_for = RandomForestClassifier(**best_params)
    val_score_rand_for = cross_val_score(rand_for, X_train, y_train, cv=3, scoring=scoring).mean()
    rand_for.fit(X_train, y_train)
    report = classification_report(y_test, rand_for.predict(X_test), digits=4, output_dict=True)
    dict_rand_for['rand_for'] = [best_params, rand_for, val_score_rand_for, report]
    prec_rand_for = float(dict_rand_for['rand_for'][3]['weighted avg']['precision'])

    return dict_rand_for, prec_rand_for


def get_advanced_models(X_train, y_train, X_test, y_test, day_, sector, model_name, path_):
    """
    This function train advanced models (Gradient Boosting and Random Forest) and choose the
    best one.

    :param X_train: Set of train features.
    :param y_train: Set of train target.
    :param X_test: Set of test features.
    :param y_test: Set of train target.
    :param int day_: Time window in execution.
    :param sector: Sector gics to predict.
    :param str or None model_name: Name of the best model. If it's None is because the model has to be trained.
    :param str path_: Path where the models are saved.
    :return tuple: Tuple of dictionary with information about the models and the best one.
    """
    t_init = time.time()
    scoring = 'precision_macro'
    dict_rand_for = {}
    dict_light = {}
    dict_total = {}
    check_ = (sector, day_)
    if (check_ != ('Financials', 3)) and (check_ != ('Financials', 5)):
        if model_name is None:
            with parallel_backend('threading'):
                rand_for = GridSearchCV(RandomForestClassifier(),
                                        param_grid={'criterion': ['gini', 'entropy'],
                                                    'max_depth': [13, 14, 15],
                                                    'min_samples_split': [2, 4],
                                                    'min_samples_leaf': [1, 2]},
                                        scoring=scoring, cv=3, n_jobs=2)
                rand_for.fit(X_train, y_train)
            best_params = rand_for.best_params_
            dict_rand_for, prec_rand_for = random_forest(best_params, X_train, y_train,
                                                             X_test, y_test, scoring, dict_rand_for)
        elif model_name == 'rand_for':
            best_params = get_best_params_from_excel(path_)
            dict_rand_for, prec_rand_for = random_forest(best_params, X_train, y_train,
                                                        X_test, y_test, scoring, dict_rand_for)
        else:
            prec_rand_for = 0
    else:
        prec_rand_for = 0
        dict_rand_for['rand_for'] = [None, None, None, None]
    show_time(t_init, time.time(), 'Time to train rand_for for %d days, %s sector and %s' % (day_, sector, scoring))

    if model_name is None:
        with parallel_backend('threading'):
            light = GridSearchCV(lgb.LGBMClassifier(),
                                 param_grid={'max_depth': [13, 14, 15],
                                             'num_leaves': [32, 42],
                                             'learning_rate': [0.1, 0.3]},
                                 scoring=scoring, cv=3, n_jobs=2)
            light.fit(X_train, y_train)
        best_params = light.best_params_
        dict_light, prec_light = lightgboost(best_params, X_train, y_train,
                                             X_test, y_test, scoring, dict_light)
    elif model_name == 'light':
        best_params = get_best_params_from_excel(path_)
        dict_light, prec_light = lightgboost(best_params, X_train, y_train,
                                             X_test, y_test, scoring, dict_light)
    else:
        prec_light = 0
    show_time(t_init, time.time(), 'Time to train light for %d days, %s sector and %s' % (day_, sector, scoring))

    if prec_rand_for >= prec_light:
        dict_total['best'] = dict_rand_for
    else:
        dict_total['best'] = dict_light

    return dict_total, dict_rand_for, dict_light
