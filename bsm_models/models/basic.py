"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains bacis models to train.

"""
from utilities.utils import get_best_params_from_excel

import time

from utilities.time import show_time
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.utils import parallel_backend


def decission_tree(best_params, X_train, y_train, X_test, y_test, scoring, dict_dec_tree, model_name):
    """
    Function to construct a dec_tree.

    :param dict best_params: A dictionary with the best params of the model.
    :param np.Array X_train: Features train data.
    :param np.Array y_train: Target train data.
    :param np.Array X_test: Features test data.
    :param np.Array y_test: Target test data.
    :param str scoring: Scoring to improve.
    :param dict dict_dec_tree: Dictionary for dec_tree output.
    :return tuple: A tuple with a dict of returns and the precision obtained.
    """
    val_score_dec_tree = 0
    dec_tree = DecisionTreeClassifier(**best_params)
    if model_name is None:
        val_score_dec_tree = cross_val_score(dec_tree, X_train, y_train, cv=3, scoring=scoring).mean()
    dec_tree.fit(X_train, y_train)
    report = classification_report(y_test, dec_tree.predict(X_test), digits=4, output_dict=True)
    if model_name is None:
        dict_dec_tree['dec_tree'] = [best_params, dec_tree, val_score_dec_tree, report]
    else:
        dict_dec_tree['dec_tree'] = [best_params, dec_tree, val_score_dec_tree, report]
    prec_dec_tree = float(dict_dec_tree['dec_tree'][3]['weighted avg']['precision'])

    return dict_dec_tree, prec_dec_tree


def k_neighbors(best_params, X_train, y_train, X_test, y_test, scoring, dict_knn):
    """
    Function to construct a knn.

    :param dict best_params: A dictionary with the best params of the model.
    :param np.Array X_train: Features train data.
    :param np.Array y_train: Target train data.
    :param np.Array X_test: Features test data.
    :param np.Array y_test: Target test data.
    :param str scoring: Scoring to improve.
    :param dict dict_knn: Dictionary for knn output.
    :return tuple: A tuple with a dict of returns and the precision obtained.
    """
    knn = KNeighborsClassifier(**best_params)
    val_score_knn = cross_val_score(knn, X_train, y_train, cv=3, scoring=scoring).mean()
    knn.fit(X_train, y_train)
    report = classification_report(y_test, knn.predict(X_test), digits=4, output_dict=True)
    dict_knn['knn'] = [best_params, knn, val_score_knn, report]
    prec_knn = float(dict_knn['knn'][3]['weighted avg']['precision'])

    return dict_knn, prec_knn


def logistic_regression(best_params, X_train, y_train, X_test, y_test, scoring, dict_log_reg):
    """
    Function to construct a logistic regression.

    :param dict best_params: A dictionary with the best params of the model.
    :param np.Array X_train: Features train data.
    :param np.Array y_train: Target train data.
    :param np.Array X_test: Features test data.
    :param np.Array y_test: Target test data.
    :param str scoring: Scoring to improve.
    :param dict dict_log_reg: Dictionary for logistic regresion output.
    :return tuple: A tuple with a dict of returns and the precision obtained.
    """
    log_reg = LogisticRegression(**best_params)
    val_score_log_reg = cross_val_score(log_reg, X_train, y_train, cv=3, scoring=scoring).mean()
    log_reg.fit(X_train, y_train)
    report = classification_report(y_test, log_reg.predict(X_test), digits=4, output_dict=True)
    dict_log_reg['log_reg'] = [best_params, log_reg, val_score_log_reg, report]
    prec_log_reg = float(dict_log_reg['log_reg'][3]['weighted avg']['precision'])

    return dict_log_reg, prec_log_reg


def get_basic_models(X_train, y_train, X_test, y_test, day_, sector, model_name, path_):
    """
    This function train basic models (Logistic Regression, KNN and Decciosion Tree) and choose the
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
    dict_log_reg = {}
    dict_knn = {}
    dict_dec_tree = {}
    dict_total = {}
    check_ = (sector, day_)
    if (check_ != ('Financials', 3)) and (check_ != ('Financials', 5)):
        if model_name is None:
            with parallel_backend('threading'):
                log_reg = GridSearchCV(LogisticRegression(),
                                       param_grid={'C': [1.2, 1, 0.8],
                                                   'tol': [1e-3, 1e-4, 1e-5],
                                                   'multi_class': ['auto']},
                                       scoring=scoring, cv=3, n_jobs=2)
                log_reg.fit(X_train, y_train)
            best_params = log_reg.best_params_
            dict_log_reg, prec_log_reg = logistic_regression(best_params, X_train, y_train,
                                                             X_test, y_test, scoring, dict_log_reg)
        elif model_name == 'log_reg':
            best_params = get_best_params_from_excel(path_)
            dict_log_reg, prec_log_reg = logistic_regression(best_params, X_train, y_train,
                                                             X_test, y_test, scoring, dict_log_reg)
        else:
            prec_log_reg = 0
            dict_log_reg['log_reg'] = [None, None, None, None]
    else:
        prec_log_reg = 0
        dict_log_reg['log_reg'] = [None, None, None, None]
    show_time(t_init, time.time(), 'Time to train log_reg for %d days, %s sector and %s' % (day_, sector, scoring))

    if model_name is None:
        with parallel_backend('threading'):
            knn = GridSearchCV(KNeighborsClassifier(),
                               param_grid={'n_neighbors': range(3, 9),
                                           'weights': ['uniform', 'distance']},
                               scoring=scoring, cv=3, n_jobs=2)
            knn.fit(X_train, y_train)
        best_params = knn.best_params_
        dict_knn, prec_knn = k_neighbors(best_params, X_train, y_train,
                                         X_test, y_test, scoring, dict_knn)
    elif model_name == 'knn':
        best_params = get_best_params_from_excel(path_)
        dict_knn, prec_knn = k_neighbors(best_params, X_train, y_train,
                                         X_test, y_test, scoring, dict_knn)
    else:
        prec_knn = 0
        dict_knn['knn'] = [None, None, None, None]
    show_time(t_init, time.time(), 'Time to train knn for %d days, %s sector and %s' % (day_, sector, scoring))

    if (check_ != ('Financials', 3)) and (check_ != ('Financials', 5)):
        if model_name is None:
            with parallel_backend('threading'):
                dec_tree = GridSearchCV(DecisionTreeClassifier(),
                                        param_grid={'criterion': ['gini', 'entropy'],
                                                    'max_depth': [13, 14, 15],
                                                    'min_samples_split': [2, 4],
                                                    'min_samples_leaf': [1, 2]},
                                        scoring=scoring, cv=3, n_jobs=2)
                dec_tree.fit(X_train, y_train)
            best_params = dec_tree.best_params_
            dict_dec_tree, prec_dec_tree = decission_tree(best_params, X_train, y_train,
                                                          X_test, y_test, scoring, dict_dec_tree, model_name)
        elif model_name == 'dec_tree':
            best_params = get_best_params_from_excel(path_)
            dict_dec_tree, prec_dec_tree = decission_tree(best_params, X_train, y_train,
                                                          X_test, y_test, scoring, dict_dec_tree, model_name)
        else:
            prec_dec_tree = 0
            dict_dec_tree['dec_tree'] = [None, None, None, None]
    else:
        prec_dec_tree = 0
        dict_dec_tree['dec_tree'] = [None, None, None, None]
    show_time(t_init, time.time(), 'Time to train dec_tree for %d days, %s sector and %s' % (day_, sector, scoring))

    if prec_log_reg >= prec_knn:
        if prec_log_reg >= prec_dec_tree:
            dict_total['best'] = dict_log_reg
        else:
            dict_total['best'] = dict_dec_tree
    else:
        if prec_knn >= prec_dec_tree:
            dict_total['best'] = dict_knn
        else:
            dict_total['best'] = dict_dec_tree

    return dict_total, dict_log_reg, dict_knn, dict_dec_tree
