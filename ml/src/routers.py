from fastapi import APIRouter, status
from model import predict
from schemas import Order

router = APIRouter()


@router.get('/health')
def health():
    return {'status': status.HTTP_200_OK}


@router.post('/pack')
def get_prediction(request: Order):
    items = []
    for el in request.items:
        if 340 not in el.cargotype:
            items.append(el.dict())
    y = predict(items)
    return {
        'orderId': request.orderkey,
        'package': y,
        'status': status.HTTP_200_OK
    }
