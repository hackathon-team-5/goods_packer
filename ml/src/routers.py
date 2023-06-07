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
COLUMNS = ['a', 'b', 'c', 'goods_wght', 'cargotype']


@router.get('/health')
def health():
    return {'status': status.HTTP_200_OK}


@router.post('/pack')
def get_prediction(request: Order):
    items = [vars(item) for item in request.items]
    df_items = pd.DataFrame.from_records(items, columns=COLUMNS)
    df_items['pack_volume'] = df_items.apply(
        lambda x: round(x['a'] * x['b'] * x['c'], 2),
        axis=1
    )
    df_items[IMPOTENT_CARGOTYPE] = ''
    for item in IMPOTENT_CARGOTYPE:
        df_items[item] = df_items.apply(
            lambda x: 1
            if int(item.split('_')[1]) in x['cargotype'] else 0,
            axis=1
        )
    df_items = df_items.drop('cargotype', axis=1)
    if len(items) == 1:
        response = predict_1_item(df_items)
    else:
        response = predict_many_items(df_items)

    return {
        'orderId': request.orderkey,
        'package': response[0],
        'status': response[1]
    }
