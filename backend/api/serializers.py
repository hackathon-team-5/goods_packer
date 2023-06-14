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


class SkuCargotypesSerializer(serializers.ModelSerializer):
    cargotype = CargotypeInfoSerializer()

    class Meta:
        model = SkuCargotypes
        fields = (
            'cargotype',
        )


class SkuSerializer(serializers.ModelSerializer):
    a = serializers.FloatField(source='length')
    b = serializers.FloatField(source='width')
    c = serializers.FloatField(source='height')
    cargotypes = SkuCargotypesSerializer(many=True, source='sku_cargotypes')

    class Meta:
        model = Sku
        fields = (
            'sku',
            'a',
            'b',
            'c',
            'goods_wght',
            'image',
            'cargotypes',
            'description'
        )


class SkuInOrderSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='sku.id')
    sku = SkuSerializer(read_only=True)

    class Meta:
        model = SkuInOrder
        fields = (
            'id',
            'sku',
            'amount',
        )


class OrderSerializer(serializers.ModelSerializer):
    skus = SkuInOrderSerializer(source='qt_skus', many=True, read_only=True)

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
            'skus',
            'who',
            'trackingid',
        )


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
    Сериализатор для создания ордеров.
    """
    orderkey = serializers.ReadOnlyField()
    sku = SkuInOrderCreateSerializer(many=True)
    trackingid = serializers.ReadOnlyField(source='id')

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
        field_list = ['whs']
        field_validator(obj, field_list)
        sku_validator(self, obj.get('sku'))
        return obj

    @transaction.atomic
    def create(self, validated_data):
        skus_data = validated_data.pop('sku')
        order = Order.objects.create(**validated_data)
        order.trackingid = order.id
        order.save()
        objs = tuple(
            SkuInOrder(
                order=order,
                sku=Sku.objects.get(sku=sku['sku']),
                amount=sku['amount'])
            for sku in skus_data
        )
        SkuInOrder.objects.bulk_create(objs)
        return order

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data
