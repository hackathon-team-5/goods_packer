import pickle

from config import BASE_DIR


def predict(x):
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
