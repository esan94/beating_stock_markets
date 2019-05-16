import os
import pandas as pd
from sklearn.externals import joblib


def get_best_params_from_excel(path_):
    """
    Function to extract the best params in the training process.

    :param str path_: Path with the saved models.
    :return dict: Dictionary with the best params.
    """

    dictf = None
    list_files = os.listdir(path_)
    for file in list_files:
        path_file = os.path.join(path_, file)
        if file.startswith('report_'):
            dictf = pd.read_excel(path_file, sheet_name='best_params').to_dict()
        os.remove(path_file)
    return dictf['best_values']


def get_best_model(path_):
    """
    This function is to load the name of the best model previously saved.

    :param str path_: Path where the model is saved.
    :return str: Name of the best model.
    """
    list_files = os.listdir(path_)
    best_model = [elem for elem in list_files if elem.endswith('.mdl')]
    return best_model[0].split('.')[0]


def get_best_ensem_model(path_):
    """
    This function is to load the model for ensembles.

    :param str path_: Path where the model is saved.
    :return: Ensemble model saved.
    """
    model = 0
    list_files = os.listdir(path_)
    for file in list_files:
        path_file = os.path.join(path_, file)
        if file.endswith('.mdl'):
            model = joblib.load(path_file)
        os.remove(path_file)
    return model
