from pathlib import Path

import pandas as pd
from api.models import (CargotypeInfo, Carton, CartonPrice, Sku, SkuCargotypes,
                        SkuInWhs, Whs)

from ._cleaners import get_image, nonzero, random_float

HOME_PATH = f'{Path.home()}/Desktop/data'


MODEL_DATA = {
    Carton: {
        'type': pd.read_csv,
        'file_name': 'carton.csv',
        'model_fields': [
            'cartontype', 'length', 'width', 'height', 'displayrfpack'
        ],
        'file_fields': [
            'CARTONTYPE', 'LENGTH', 'WIDTH', 'HEIGHT', 'DISPLAYRFPACK'
        ],
        'cleaner': [
            str, float, float, float, bool
        ],
        'getter': [
            None, None, None, None, None
        ],
    },
    CartonPrice: {
        'type': pd.read_excel,
        'file_name': 'carton_price.xlsx',
        'model_fields': ['carton', 'price'],
        'file_fields': ['carton', 'cost'],
        'cleaner': [str, float],
        'getter': [
            [Carton, 'cartontype'], None
        ],
    },
    CargotypeInfo: {
        'type': pd.read_csv,
        'file_name': 'cargotype_info.csv',
        'model_fields': ['cargotype', 'description'],
        'file_fields': ['cargotype', 'description'],
        'cleaner': [int, str],
        'getter': [None, None],
    },
    Sku: {
        'type': pd.read_csv,
        'file_name': 'sku.csv',
        'model_fields': ['sku', 'length', 'width', 'height', 'goods_wght', 'image'],
        'file_fields': ['sku', 'a', 'b', 'c', 'weight', 'image'],
        'cleaner': [str, nonzero, nonzero, nonzero, random_float, get_image],
        'getter': [None, None, None, None, None, None],
    },
    SkuCargotypes: {
        'type': pd.read_csv,
        'file_name': 'sku_cargotypes.csv',
        'model_fields': ['sku', 'cargotype'],
        'file_fields': ['sku', 'cargotype'],
        'cleaner': [str, int],
        'getter': [[Sku, 'sku'], [CargotypeInfo, 'cargotype']],
    },
    Whs: {
        'type': pd.read_csv,
        'file_name': 'whs.csv',
        'model_fields': ['whs'],
        'file_fields': ['whs'],
        'cleaner': [str],
        'getter': [None],
    },
    SkuInWhs: {
        'type': pd.read_csv,
        'file_name': 'skuinwhs.csv',
        'model_fields': ['sku', 'whs', 'amount'],
        'file_fields': ['sku', 'whs', 'count'],
        'cleaner': [str, str, random_float],
        'getter': [[Sku, 'sku'], [Whs, 'whs'], None],
    },
}


def convert_to_models():
    """
    The function reads the files for each model in MODEL_DATA, cleans the data
    using the cleaner function, retrieves related data using the getter
    function, creates model instances using the cleaned data, and bulk creates
    them in the database.

    If any error occurs during the process, it is added to the result list
    and returned at the end.
    """
    result = []
    for model, model_data in MODEL_DATA.items():
        try:
            data = model_data['type'](f'{HOME_PATH}/{model_data["file_name"]}')
            clean_data = []
            for _, row in data.iterrows():
                clean_row = model(**{
                    model_fields: (
                        getter[0].objects.get_or_create(**{getter[1]: row[file_field]})[0]
                        if getter else cleaner(row[file_field])
                    )
                    for model_fields, file_field, cleaner, getter in zip(
                        model_data['model_fields'],
                        model_data['file_fields'],
                        model_data['cleaner'],
                        model_data['getter']
                    )
                })
                clean_data.append(clean_row)
            model.objects.bulk_create(clean_data)
        except Exception as error:
            result.extend(['error', f'{model}: {error}'])
    return result
