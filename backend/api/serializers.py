import json
import uuid
from typing import OrderedDict

import requests
from core.validators import field_validator, sku_validator
from django.db import transaction
from rest_framework import serializers

from .models import (CargotypeInfo, Carton, CartonPrice, Order, Sku,
                     SkuCargotypes, SkuInOrder)


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
    Additional sku serializer.
    """
    sku = serializers.CharField()

    class Meta:
        model = SkuInOrder
        fields = ('sku', 'amount')


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders.
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
        Validating.
        """
        field_list = ['whs']
        field_validator(obj, field_list)
        sku_validator(self, obj.get('sku'))
        return obj

    @transaction.atomic
    def create(self, validated_data):
        """
        Creating and enriching an order.
        """
        skus_data = validated_data.pop('sku')
        order = Order.objects.create(**validated_data)
        objs = []
        ml_pack = {
            'orderkey': order.id,
            'items': []
        }
        for sku in skus_data:
            sku_inst = Sku.objects.get(
                sku=sku['sku']
            )
            ml_pack['items'].append(
                {
                    'sku': sku_inst.sku,
                    'count': sku.get('amount'),
                    'a': sku_inst.length,
                    'b': sku_inst.width,
                    'c': sku_inst.height,
                    'goods_wght': sku_inst.goods_wght,
                    'pack_volume': round(
                        sku_inst.length * sku_inst.width * sku_inst.height,
                        2
                    ),
                    'cargotype': list(
                        sku_inst.sku_cargotypes.values_list(
                            'cargotype', flat=True
                        )
                    )
                }
            )
            order.goods_wght += sku_inst.goods_wght
            order.pack_volume += ml_pack['items'][-1]['pack_volume']
            objs.append(
                SkuInOrder(
                    order=order,
                    sku=sku_inst,
                    amount=sku['amount']
                )
            )
        SkuInOrder.objects.bulk_create(objs)
        order.trackingid = order.id
        order.orderkey = uuid.uuid4
        response = requests.post(
            url="http://127.0.0.1:8080/pack/",
            json=ml_pack)
        model_prediction = json.loads(response.text).get('package', None)
        if model_prediction and isinstance(model_prediction, str):
            order.recommended_cartontype = Carton.objects.filter(
                cartontype=model_prediction
            ).first()
        order.save()
        return order

    def to_representation(self, instance):
        representation = OrderSerializer(instance, context=self.context).data
        representation['recommended_cartontype'] = (
            instance.recommended_cartontype.cartontype
        )
        return representation
