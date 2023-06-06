from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    sku: str
    count: int
    a: float
    b: float
    c: float
    goods_wght: float
    cargotype: List[int]


class Order(BaseModel):
    orderkey: str
    items: List[Item]
