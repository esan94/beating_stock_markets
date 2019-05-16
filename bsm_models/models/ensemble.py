"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains ensemble models to train.

"""
from utilities.utils import get_best_ensem_model

import time

from utilities.time import show_time
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import VotingClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.utils import parallel_backend


def get_ensemble_models(X_train, y_train, X_test, y_test, day_, sector, best_params, model_name, path_):
    """
    This function is to looking for the best ensemble model.
    
    :param X_train: Set of features for train.
    :param y_train: Set of target for train.
    :param X_test: Set of features for test.
    :param y_test: Set of target for test.
    :param int day_: Time window for features.
    :param str sector: Sector GICS for filtering the predictions.
    :param list best_params: List of best params for basics models.
    :param str or None model_name: Name of the best model. If it's None is because the model has to be trained.
    :param str path_: Path where the models are saved.
    :return tuple of dict: Tuple of dicts with the different models.
    """
    t_init = time.time()
    scoring = 'precision_macro'
    dict_vot = {}
    dict_bagg = {}
    dict_ada = {}
    dict_total = {}
    check_ = (sector, day_)
    if (check_ != ('Financials', 3)) and (check_ != ('Financials', 5)):
        if model_name is None:
            with parallel_backend('threading', n_jobs=2):
                vot = VotingClassifier(estimators=[('DecTree', DecisionTreeClassifier(**best_params[2])),
                                                   ('KNN', KNeighborsClassifier(**best_params[1])),
                                                   ('LogReg', LogisticRegression(**best_params[0]))])
                val_score_vot = cross_val_score(vot, X_train, y_train, cv=3, scoring=scoring).mean()
                vot.fit(X_train, y_train)
            report = classification_report(y_test, vot.predict(X_test), digits=4, output_dict=True)
            dict_vot['vot'] = [vot, val_score_vot, report]
            prec_vot = float(dict_vot['vot'][2]['weighted avg']['precision'])
        elif model_name == 'vot':
            vot = get_best_ensem_model(path_)
            vot.fit(X_train, y_train)
            report = classification_report(y_test, vot.predict(X_test), digits=4, output_dict=True)
            dict_vot['vot'] = [vot, report]
            prec_vot = float(dict_vot['vot'][1]['weighted avg']['precision'])
        else:
            prec_vot = 0
    else:
        prec_vot = 0
    show_time(t_init, time.time(), 'Time to train vot for %d days, %s sector and %s' % (day_, sector, scoring))

    if model_name is None:
        with parallel_backend('threading', n_jobs=2):
            bagg = BaggingClassifier(base_estimator=KNeighborsClassifier(**best_params[1]))
            val_score_bagg = cross_val_score(bagg, X_train, y_train, cv=3, scoring=scoring).mean()
            bagg.fit(X_train, y_train)
        report = classification_report(y_test, bagg.predict(X_test), digits=4, output_dict=True)
        dict_bagg['bagg'] = [bagg, val_score_bagg, report]
        prec_bagg = float(dict_bagg['bagg'][2]['weighted avg']['precision'])
    elif model_name == 'bagg':
        bagg = get_best_ensem_model(path_)
        bagg.fit(X_train, y_train)
        report = classification_report(y_test, bagg.predict(X_test), digits=4, output_dict=True)
        dict_bagg['bagg'] = [bagg, report]
        prec_bagg = float(dict_bagg['bagg'][1]['weighted avg']['precision'])
    else:
        prec_bagg = 0
    show_time(t_init, time.time(), 'Time to train bagg for %d days, %s sector and %s' % (day_, sector, scoring))

    if (check_ != ('Financials', 3)) and (check_ != ('Financials', 5)):
        if model_name is None:
            with parallel_backend('threading', n_jobs=2):
                ada = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(**best_params[2]))
                val_score_ada = cross_val_score(ada, X_train, y_train, cv=3, scoring=scoring).mean()
                ada.fit(X_train, y_train)
            report = classification_report(y_test, ada.predict(X_test), digits=4, output_dict=True)
            dict_ada['ada'] = [ada, val_score_ada, report]
            prec_ada = float(dict_ada['ada'][2]['weighted avg']['precision'])
        elif model_name == 'ada':
            ada = get_best_ensem_model(path_)
            ada.fit(X_train, y_train)
            report = classification_report(y_test, ada.predict(X_test), digits=4, output_dict=True)
            dict_ada['ada'] = [ada, report]
            prec_ada = float(dict_ada['ada'][1]['weighted avg']['precision'])
        else:
            prec_ada = 0
    else:
        prec_ada = 0
    show_time(t_init, time.time(), 'Time to train ada for %d days, %s sector and %s' % (day_, sector, scoring))

    if prec_vot >= prec_bagg:
        if prec_vot >= prec_ada:
            dict_total['best'] = dict_vot
        else:
            dict_total['best'] = dict_ada
    else:
        if prec_bagg >= prec_ada:
            dict_total['best'] = dict_bagg
        else:
            dict_total['best'] = dict_ada

    return dict_total, dict_vot, dict_bagg, dict_ada
