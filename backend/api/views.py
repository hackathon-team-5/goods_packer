from rest_framework import viewsets, permissions

from .models import Sku, Order, Carton, CargotypeInfo, CartonPrice
from .serializzers import CartonSerializer, CargotypeInfoSerializer, \
    CartonPriceSerializer, SkuSerializer, SkuCargotypesSerializer, \
    OrderSerializer


class CartonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carton.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CartonSerializer


class CargotypeInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargotypeInfo.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CargotypeInfoSerializer


class CartonPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CartonPrice.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CartonPriceSerializer


class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sku.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SkuSerializer


class SkuCargotypesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SkuCargotypesSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer
