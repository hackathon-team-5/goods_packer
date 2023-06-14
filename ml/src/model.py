import pickle

import numpy as np
from config import BASE_DIR
from fastapi import status


def predict_1_item(x):
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
