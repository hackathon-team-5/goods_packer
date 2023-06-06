import pickle

import numpy as np
from config import BASE_DIR


def predict_1_item(x):
    """
    The function attempts to load a pre-trained machine learning model from
    a pickle file located in the "trained_model" directory. If the model
    cannot be loaded, an exception is raised. The function then uses the
    loaded model to make a prediction on the input "x" and returns the result.
    If an error occurs during the prediction process, the function returns an
    error message.
    """
    try:
        with open(f'{BASE_DIR}/src/trained_model/model1.pcl', 'rb') as fid:
            model = pickle.load(fid)
    except OSError:
        raise Exception('Failed to open the model file')

    try:
        result = model.predict(x)
    except Exception as error:
        return f'Predict: {error}'

    return result


def predict_many_items(x):
    """
    The function takes an input "x" and loads two trained models from files.
    It then uses the first model to make a prediction on "x" and appends the
    result to "x". Finally, it uses the second model to make a prediction on
    the updated "x". If any errors occur during the process, it returns an
    error message. Otherwise, it returns the predicted result.
    """
    try:
        with open(f'{BASE_DIR}/src/trained_model/model2.pcl', 'rb') as fid:
            model2 = pickle.load(fid)

        with open(f'{BASE_DIR}/src/trained_model/model3.pcl', 'rb') as fid:
            model3 = pickle.load(fid)

    except OSError:
        raise Exception('Failed to open the model file')

    try:
        result_1 = model2.predict(x)

        x_1 = np.column_stack((x, result_1))

        result = model3.predict(x_1)

    except Exception as error:
        return f'Predict: {error}'

    return result
