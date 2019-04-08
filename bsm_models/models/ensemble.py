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
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import VotingClassifier, BaggingClassifier, AdaBoostClassifier


def get_ensemble_models(X_train, y_train, X_test, y_test, day_, sector, best_params):
    scoring = 'precision_macro'
    dict_vot = {}
    dict_bagg = {}
    dict_ada = {}
    dict_total = {}

    print('Time to train vot for %d days, %s sector and %s' % (day_, sector, scoring))
    vot = VotingClassifier(estimators=[('DecTree', DecisionTreeClassifier(**best_params[2])),
                                       ('KNN', KNeighborsClassifier(**best_params[1])),
                                       ('LogReg', LogisticRegression(**best_params[0]))])
    val_score_vot = cross_val_score(vot, X_train, y_train, cv=5, scoring=scoring).mean()
    vot.fit(X_train, y_train)
    report = classification_report(y_test, vot.predict(X_test), digits=4, output_dict=True)
    dict_vot['vot'] = [vot, val_score_vot, report]
    print(classification_report(y_test, vot.predict(X_test), digits=4))

    print('Time to train bagg for %d days, %s sector and %s' % (day_, sector, scoring))
    bagg = BaggingClassifier(base_estimator=KNeighborsClassifier(**best_params[1]))
    val_score_bagg = cross_val_score(bagg, X_train, y_train, cv=5, scoring=scoring).mean()
    bagg.fit(X_train, y_train)
    report = classification_report(y_test, bagg.predict(X_test), digits=4, output_dict=True)
    dict_bagg['bagg'] = [bagg, val_score_bagg, report]
    print(classification_report(y_test, bagg.predict(X_test), digits=4))

    print('Time to train ada for %d days, %s sector and %s' % (day_, sector, scoring))
    ada = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(**best_params[2]))
    val_score_ada = cross_val_score(ada, X_train, y_train, cv=5, scoring=scoring).mean()
    ada.fit(X_train, y_train)
    report = classification_report(y_test, ada.predict(X_test), digits=4, output_dict=True)
    dict_ada['ada'] = [ada, val_score_ada, report]
    print(classification_report(y_test, ada.predict(X_test), digits=4))

    prec_vot = int(dict_vot['vot'][2]['weighted avg']['precision'])
    prec_bagg = int(dict_bagg['bagg'][2]['weighted avg']['precision'])
    prec_ada = int(dict_ada['ada'][2]['weighted avg']['precision'])

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

