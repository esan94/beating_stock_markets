import pandas as pd


def get_correlated_columns(X_train, features_col):
    """
    Calculate the correlation matrix between features and give the most correlated features.

    :param X_train: Train data for calculate correlation.
    :param list features_col: List with the name of the columns of the train data.
    :return dict: Dictinary where keys are columns and values a list of the most correlated features.
    """
    df_ = pd.DataFrame(data=X_train, columns=features_col)
    df_ = df_.corr()
    df_ = df_.drop('close', axis=1)
    df_ = df_.drop('close', axis=0)
    dict_ = {}
    df__ = df_[df_.abs() >=.9]
    df__ = df__[df__ < 1].dropna(axis=1, how='all').dropna(axis=0, how='all')
    list_ = list(df__.columns)
    for col in list_:
        dict_[col] = list(df__[df__[col].notnull()].index)
        for elem in dict_[col]:
            if elem in list_:
                list_.remove(elem)
    return dict_
