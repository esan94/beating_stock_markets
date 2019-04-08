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
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score

def get_basic_models(X_train, y_train, X_test, y_test, day_, sector):
    scoring = 'precision_macro'
    dict_log_reg = {}
    dict_knn = {}
    dict_dec_tree = {}
    dict_total = {}

    log_reg = GridSearchCV(LogisticRegression(),
                           param_grid={'C': [1.2, 1, 0.8],
                                       'tol': [1e-3, 1e-4, 1e-5],
                                       'multi_class': ['auto']},
                           scoring=scoring, cv=5)
    print('Time to train log_reg for %d days, %s sector and %s' % (day_, sector, scoring))
    log_reg.fit(X_train, y_train)
    best_params = log_reg.best_params_
    log_reg = LogisticRegression(**log_reg.best_params_)
    val_score_log_reg = cross_val_score(log_reg, X_train, y_train, cv=5, scoring=scoring).mean()
    log_reg.fit(X_train, y_train)
    report = classification_report(y_test, log_reg.predict(X_test), digits=4, output_dict=True)
    dict_log_reg['log_reg'] = [best_params, log_reg, val_score_log_reg, report]

    knn = GridSearchCV(KNeighborsClassifier(),
                       param_grid={'n_neighbors': range(3, 9),
                                   'weights': ['uniform', 'distance']},
                       scoring=scoring, cv=5)
    print('Time to train knn for %d days, %s sector and %s' % (day_, sector, scoring))
    knn.fit(X_train, y_train)
    best_params = knn.best_params_
    knn = KNeighborsClassifier(**knn.best_params_)
    val_score_knn = cross_val_score(knn, X_train, y_train, cv=5, scoring=scoring).mean()
    knn.fit(X_train, y_train)
    report = classification_report(y_test, knn.predict(X_test), digits=4, output_dict=True)
    dict_knn['knn'] = [best_params, knn, val_score_knn, report]

    dec_tree = GridSearchCV(DecisionTreeClassifier(),
                            param_grid={'criterion': ['gini', 'entropy'],
                                        'max_depth': [13, 14, 15],
                                        'min_samples_split': [2, 4],
                                        'min_samples_leaf': [1, 2]},
                            scoring=scoring, cv=5)
    print('Time to train dec_tree for %d days, %s sector and %s' % (day_, sector, scoring))
    dec_tree.fit(X_train, y_train)
    best_params = dec_tree.best_params_
    dec_tree = DecisionTreeClassifier(**dec_tree.best_params_)
    val_score_dec_tree = cross_val_score(dec_tree, X_train, y_train, cv=5, scoring=scoring).mean()
    dec_tree.fit(X_train, y_train)
    report = classification_report(y_test, dec_tree.predict(X_test), digits=4, output_dict=True)
    dict_dec_tree['dec_tree'] = [best_params, dec_tree, val_score_dec_tree, report]

    prec_log_reg = int(dict_log_reg['log_reg'][3]['weighted avg']['precision'])
    prec_knn = int(dict_knn['knn'][3]['weighted avg']['precision'])
    prec_dec_tree = int(dict_dec_tree['dec_tree'][3]['weighted avg']['precision'])

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
