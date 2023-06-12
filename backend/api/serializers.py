from typing import OrderedDict

from core.validators import field_validator, sku_validator
from django.db import transaction
from rest_framework import serializers

from .models import (CargotypeInfo, Carton, CartonPrice, Order, Sku,
                     SkuCargotypes, SkuInOrder, SkuInWhs, Whs)


class CartonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carton
        fields = (
            'cartontype',
            'length',
            'width',
            'height',
            'displayrfpack'
        )


class CargotypeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CargotypeInfo
        fields = (
            'cargotype',
            'description'
        )


class CartonPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartonPrice
        fields = (
            'carton',
            'price'
        )


class SkuSerializer(serializers.ModelSerializer):
    a = serializers.FloatField(source='length')
    b = serializers.FloatField(source='width')
    c = serializers.FloatField(source='height')

    class Meta:
        model = Sku
        fields = (
            'sku',
            'a',
            'b',
            'c',
            'goods_wght',
            'image',
            'description'
        )


class SkuCargotypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkuCargotypes
        fields = (
            'sku',
            'cargotype'
        )


class SkuInOrderSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='sku.id')
    sku = serializers.ReadOnlyField(source='sku.sku')

    class Meta:
        model = SkuInOrder
        fields = (
            'id',
            'sku',
            'amount',
        )


class OrderSerializer(serializers.ModelSerializer):
    skus = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'whs',
            'orderkey',
            'selected_cartontype',
            'box_num',
            'recommended_cartontype',
            'sel_calc_cube',
            'pack_volume',
            'rec_calc_cube',
            'goods_wght',
            'sku',
            'who',
            'trackingid',
        )

    def get_skus(self, obj: Sku) -> OrderedDict:

        queryset = obj.qt_skus.all()
        return SkuInOrderSerializer(queryset, many=True).data


class SkuInOrderCreateSerializer(serializers.ModelSerializer):
    """
    Дополнительный сериализатор sku для поля sku.
    """
    sku = serializers.CharField()

    class Meta:
        model = SkuInOrder
        fields = ('sku', 'amount')


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения ордеров.
    """
    orderkey = serializers.ReadOnlyField()
    sku = SkuInOrderCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'whs',
            'orderkey',
            'selected_cartontype',
            'box_num',
            'recommended_cartontype',
            'sel_calc_cube',
            'pack_volume',
            'rec_calc_cube',
            'goods_wght',
            'sku',
            'who',
            'trackingid',
            'status',
        )

    def validate(self, obj: OrderedDict) -> OrderedDict:
        """
        Валидация полей.
        """
        field_list = ['whs', 'who']
        field_validator(obj, field_list)
        sku_validator(self, obj.get('sku'))
        return obj

    @transaction.atomic
    def create(self, validated_data):
        skus_data = validated_data.pop('sku')
        order = Order.objects.create(**validated_data)
        objs = tuple(
            SkuInOrder(
                order=order,
                sku=Sku.objects.get(sku=sku['sku']),
                amount=sku['amount'])
            for sku in skus_data
        )
        SkuInOrder.objects.bulk_create(objs)
        return order
