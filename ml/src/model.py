import pickle

import numpy as np
from config import BASE_DIR
from fastapi import status


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
        result = (model.predict(x), status.HTTP_200_OK)
    except OSError as error:
        result = (
            f'Failed to open the model file: {error}',
            status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as error:
        result = (
            f'Error in predict_1_item: {error}',
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
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
        result_first = model2.predict(x)

        x_1 = np.column_stack((x, result_first))

        with open(f'{BASE_DIR}/src/trained_model/model3.pcl', 'rb') as fid:
            model3 = pickle.load(fid)
        result = (model3.predict(x_1), status.HTTP_200_OK)

    except OSError as error:
        result = (
            f'Failed to open the model file: {error}',
            status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as error:
        result = (
            f'Error in predict_many_items: {error}',
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        return result
