from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import CargotypeInfo, Carton, CartonPrice, Order, Sku
from .serializers import (CargotypeInfoSerializer, CartonPriceSerializer,
                          CartonSerializer, OrderCreateSerializer,
                          SkuCargotypesSerializer, SkuSerializer)


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderCreateSerializer
