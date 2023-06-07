import numpy as np
import pandas as pd
from fastapi import APIRouter, status
from model import predict_1_item, predict_many_items
from schemas import Order

router = APIRouter()

IMPOTENT_CARGOTYPE = [
    'cargotype_20', 'cargotype_210', 'cargotype_303',
    'cargotype_310', 'cargotype_315', 'cargotype_340',
    'cargotype_360', 'cargotype_910'
]


@router.get('/health')
def health():
    return {'status': status.HTTP_200_OK}


@router.post('/pack')
def get_prediction(request: Order):
    items = request.items
    df_items = pd.DataFrame(
        items, columns=[
            'sku', 'count', 'a', 'b', 'c', 'goods_wght', 'cargotype'
        ]
    )
    df_items[IMPOTENT_CARGOTYPE] = ''
    cargotypes = [20, 910, 315, 340, 310, 360, 210, 303]

    for item in range(len(cargotypes)):
        column_name = 'cargotype_' + str(cargotypes[item])
        amount = cargotypes[item]
        df_items[column_name] = np.where(
            df_items['cargotype'].apply(lambda x: amount in x), 1, 0
        )

    df_items = df_items.drop('cargotype', axis=1)
    df_items['pack_volume'] = df_items.apply(
        lambda x: round(x['a'][1] * x['b'][1] * x['c'][1], 2),
        axis=1
    )
    if len(items) == 1:
        df_items = df_items.drop('count', axis=1)
        response = predict_1_item(df_items)
    else:
        df_items = df_items.rename(
            columns={'count': 'count_items'}
        )
        response = predict_many_items(df_items)

    return {
        'orderId': request.orderkey,
        'package': response[0],
        'status': response[1]
    }
