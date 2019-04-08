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
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
import lightgbm as lgb


def get_advanced_models(X_train, y_train, X_test, y_test, day_, sector):
    scoring = 'precision_macro'
    dict_rand_for = {}
    dict_light = {}
    dict_total = {}

    rand_for = GridSearchCV(RandomForestClassifier(),
                            param_grid={'criterion': ['gini', 'entropy'],
                                        'max_depth': [13, 14, 15],
                                        'min_samples_split': [2, 4],
                                        'min_samples_leaf': [1, 2]},
                            scoring=scoring, cv=5)
    print('Time to train rand_for for %d days, %s sector and %s' % (day_, sector, scoring))
    rand_for.fit(X_train, y_train)
    best_params = rand_for.best_params_
    rand_for = RandomForestClassifier(**rand_for.best_params_)
    val_score_rand_for = cross_val_score(rand_for, X_train, y_train, cv=5, scoring=scoring).mean()
    rand_for.fit(X_train, y_train)
    report = classification_report(y_test, rand_for.predict(X_test), digits=4, output_dict=True)
    dict_rand_for['rand_for'] = [best_params, rand_for, val_score_rand_for, report]
    print(classification_report(y_test, rand_for.predict(X_test), digits=4))

    light = GridSearchCV(lgb.LGBMClassifier(),
                         param_grid={'max_depth': [13, 14, 15],
                                     'num_leaves': [32, 42],
                                     'learning_rate': [0.1, 0.3]},
                         scoring=scoring, cv=5)
    print('Time to train light for %d days, %s sector and %s' % (day_, sector, scoring))
    light.fit(X_train, y_train)
    best_params = light.best_params_
    light = lgb.LGBMClassifier(**light.best_params_)
    val_score_light = cross_val_score(light, X_train, y_train, cv=5, scoring=scoring).mean()
    light.fit(X_train, y_train)
    report = classification_report(y_test, light.predict(X_test), digits=4, output_dict=True)
    dict_light['light'] = [best_params, light, val_score_light, report]
    print(classification_report(y_test, light.predict(X_test), digits=4))

    prec_rand_for = int(dict_rand_for['rand_for'][3]['weighted avg']['precision'])
    prec_light = int(dict_light['light'][3]['weighted avg']['precision'])

    if prec_rand_for >= prec_light:
        dict_total['best'] = dict_rand_for
    else:
        dict_total['best'] = dict_light

    return dict_total, dict_rand_for, dict_light
