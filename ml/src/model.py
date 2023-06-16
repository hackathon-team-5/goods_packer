import pickle

import numpy as np
import pandas as pd
from config import BASE_DIR
from fastapi import status
from sklearn.calibration import LabelEncoder

PACKS = {
    'target': [
        'STRETCH', 'NONPACK', 'MYC', 'MYE', 'error', 'YMA', 'MYA', 'MYB',
        'MYD', 'YMG', 'MYF', 'YMC', 'YMW', 'YMF', 'YME', 'YMX', 'YMU', 'YMB',
        'YMV', 'YMI', 'YMT', 'YMP']
}


def predict_1_item(x):
    label_encoder = LabelEncoder()
    target = pd.DataFrame.from_dict(PACKS)
    label_encoder.fit_transform(target)
    try:
        with open(f'{BASE_DIR}/src/trained_model/model1.pcl', 'rb') as fid:
            model = pickle.load(fid)
        prediction = model.predict(x)
        result = (
            label_encoder.inverse_transform(prediction[0])[0],
            status.HTTP_200_OK
        )
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
    label_encoder = LabelEncoder()
    target = pd.DataFrame.from_dict(PACKS)
    label_encoder.fit_transform(target)
    try:
        with open(f'{BASE_DIR}/src/trained_model/model2.pcl', 'rb') as fid:
            model3 = pickle.load(fid)
        prediction = model3.predict(x)
        result = (
            label_encoder.inverse_transform(prediction[0])[0],
            status.HTTP_200_OK
        )
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
