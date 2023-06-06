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
    items = []
    df_items = pd.DataFrame(
        items, columns=[
            'sku', 'count', 'a', 'b', 'c', 'goods_wght', 'cargotype'
        ]
    )
    for column in IMPOTENT_CARGOTYPE:
        df_items[column] = ""

    cargotypes = [20, 910, 315, 340, 310, 360, 210, 303]

    for item in range(len(cargotypes)):
        column_name = 'cargotype_' + str(cargotypes[item])
        amount = cargotypes[item]
        df_items[column_name] = df_items.apply(
            lambda x: 1 if amount in x['cargotype'] else 0, axis=1
        )

    df_items = df_items.rename(
        columns={'count': 'count_items'}
    )
    df_items = df_items.drop('cargotype', axis=1)

    df_items['pack_volume'] = (
        df_items['a'] * df_items['b'] * df_items['c']
    ).astype('int')

    if len(items) == 1:
        y = predict_1_item(df_items.drop('count_items'))
    else:
        y = predict_many_items(df_items)

    return {
        'orderId': request.orderkey,
        'package': y,
        'status': status.HTTP_200_OK
    }
