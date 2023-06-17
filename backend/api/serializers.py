import json
import uuid
from collections import defaultdict
from typing import OrderedDict

import requests
from core.validators import field_validator, sku_validator
from django.db import transaction
from django.db.models import Sum
from rest_framework import serializers

from .models import (CargotypeInfo, Carton, CartonPrice, Order, Sku,
                     SkuCargotypes, SkuInOrder)

CARTON_NON_PACK = {
    360: 'STRETCH',
    340: 'NONPACK',
}


class CartonSerializer(serializers.ModelSerializer):
    """
    Carton serializer.
    """

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
    """
    Cargotype serializer.
    """

    class Meta:
        model = CargotypeInfo
        fields = (
            'cargotype',
            'description'
        )


class CartonPriceSerializer(serializers.ModelSerializer):
    """
    Serializer of the linked CartonPrice model.
    """

    class Meta:
        model = CartonPrice
        fields = (
            'carton',
            'price'
        )


class SkuCargotypesSerializer(serializers.ModelSerializer):
    """
    Serializer of the linked SkuCargotypes model.
    """
    cargotype = CargotypeInfoSerializer()

    class Meta:
        model = SkuCargotypes
        fields = (
            'cargotype',
        )


class SkuSerializer(serializers.ModelSerializer):
    """
    Basic sku serializer
    """
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


class ExpandedSkuInOrderSerializer(serializers.ModelSerializer):
    """
    Extended serializer of sku representation in the order.
    """
    id = serializers.ReadOnlyField(source='sku.id')
    sku = SkuSerializer(read_only=True)
    recommended_cartontype = CartonSerializer(read_only=True)
    selected_cartontype = CartonSerializer(read_only=True)

    class Meta:
        model = SkuInOrder
        fields = (
            'id',
            'sku',
            'amount',
            'recommended_cartontype',
            'selected_cartontype'
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Basic order serializer.
    """
    skus = ExpandedSkuInOrderSerializer(
        source='qt_skus', many=True, read_only=True
    )

    class Meta:
        model = Order
        fields = (
            'whs',
            'orderkey',
            'box_num',
            'sel_calc_cube',
            'pack_volume',
            'rec_calc_cube',
            'goods_wght',
            'skus',
            'who',
            'trackingid',
            'status',
        )


class SkuInOrderCreateSerializer(serializers.ModelSerializer):
    """
    Additional sku serializer.
    """
    sku = serializers.CharField()
    selected_cartontype = serializers.CharField(required=False)

    class Meta:
        model = SkuInOrder
        fields = (
            'sku',
            'amount',
            'selected_cartontype',
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders.
    """
    orderkey = serializers.ReadOnlyField()
    skus = SkuInOrderCreateSerializer(many=True)
    trackingid = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Order
        fields = (
            'whs',
            'orderkey',
            'box_num',
            'sel_calc_cube',
            'pack_volume',
            'rec_calc_cube',
            'goods_wght',
            'skus',
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
        sku_validator(self, obj.get('skus'))
        return obj

    @transaction.atomic
    def create(self, validated_data):
        """
        Creating and enriching an order.
        """
        skus_data = validated_data.pop('skus')
        order = Order.objects.create(**validated_data)
        ml_pack = self._create_ml_pack(order, skus_data)
        self._update_order_properties(order, ml_pack)
        self._create_sku_in_order_objects(order, skus_data)
        self._update_order_with_tracking_and_key(order)
        self._update_recommended_cartontypes(order, ml_pack)
        order.save()
        return order

    @classmethod
    def _create_ml_pack(cls, order, skus_data):
        """
        Creates a data structure `ml_pack`,
        which will be sent to the server for processing.
        """
        ml_pack = {
            'orderkey': order.id,
            'items': []
        }
        for sku in skus_data:
            sku_inst = Sku.objects.get(sku=sku['sku'])
            ml_pack['items'].append({
                'sku': sku_inst.sku,
                'count': sku.get('amount'),
                'a': sku_inst.length,
                'b': sku_inst.width,
                'c': sku_inst.height,
                'goods_wght': sku_inst.goods_wght,
                'pack_volume': round(
                    sku_inst.length * sku_inst.width * sku_inst.height, 2
                ),
                'cargotype': list(
                    sku_inst.sku_cargotypes.values_list('cargotype', flat=True)
                )
            })
        return ml_pack

    @classmethod
    def _update_order_properties(cls, order, ml_pack):
        """
        Updates `order` properties, such as `goods_wght` and `pack_volume`,
        based on data from `ml_pack`.
        """
        for item in ml_pack['items']:
            order.goods_wght += round(item['goods_wght'], 2)
            order.pack_volume += item['pack_volume']

    @classmethod
    def _create_sku_in_order_objects(cls, order, skus_data):
        """
        Creates `SkuInOrder` objects and links them to the order.
        """
        objs = []
        for sku in skus_data:
            sku_inst = Sku.objects.get(sku=sku['sku'])
            cartontype_list = sku_inst.sku_cargotypes.values_list(
                'cargotype__cargotype', flat=True
            ).all()
            cartontype = next(
                (
                    CARTON_NON_PACK[item] for item in cartontype_list
                    if item in CARTON_NON_PACK
                ),
                None
            )
            objs.append(SkuInOrder(
                order=order,
                sku=sku_inst,
                amount=sku['amount'],
                recommended_cartontype=(
                    Carton.objects.get(cartontype=cartontype)
                    if cartontype else None
                ),
            ))
        SkuInOrder.objects.bulk_create(objs)

    @classmethod
    def _update_order_with_tracking_and_key(cls, order):
        """
        Updates the `trackingid` and `orderkey` properties.
        """
        order.trackingid = order.id
        order.orderkey = uuid.uuid4

    @classmethod
    def _update_recommended_cartontypes(cls, order, ml_pack):
        """
        Updates the recommended box type `recommended_cartontype`
        for items in the order.
        """
        response = requests.post(
            url="http://127.0.0.1:8080/pack/",
            json=ml_pack
        )
        model_prediction = json.loads(response.text).get('package', None)

        if model_prediction and isinstance(model_prediction, str):
            cartontype = Carton.objects.filter(
                cartontype=model_prediction
            ).first()
            SkuInOrder.objects.filter(
                order=order, recommended_cartontype__isnull=True
            ).update(recommended_cartontype=cartontype)

    def update(self, instance, validated_data):
        """
        Updating the order.
        """
        skus_data = validated_data.pop('skus', [])
        sku_amounts = defaultdict(int)
        sku_qs = instance.qt_skus.all().select_related(
            'recommended_cartontype'
        )
        for sku_data in skus_data:
            sku = sku_data['sku']
            amount = sku_data['amount']
            sku_amounts[sku] += amount

        for sku, amount in sku_amounts.items():
            sku_qs = instance.qt_skus.filter(sku__sku=sku)
            total_amount = sku_qs.aggregate(
                total_amount=Sum('amount')
            )['total_amount']
            if amount != total_amount:
                raise serializers.ValidationError(
                    f'{sku} does not have the amount that is in {instance.id}.'
                )
            sku_in_order_data = []
            for sku_data in skus_data:
                if sku_data.get('sku') == sku:
                    selected_cartontype = sku_data.get('selected_cartontype')
                    recommended_cartontype = (
                        sku_qs.first().recommended_cartontype
                    )
                    carton = Carton.objects.filter(
                        cartontype=selected_cartontype
                    ).first()
                    sku_in_order_data.append({
                        'sku': sku_qs.first().sku,
                        'amount': sku_data.get('amount'),
                        'recommended_cartontype': recommended_cartontype,
                        'selected_cartontype': carton
                    })

            sku_qs.delete()
            SkuInOrder.objects.bulk_create(
                [
                    SkuInOrder(order=instance, **data)
                    for data in sku_in_order_data
                ]
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Converts an instance of the instance model into a data representation
        that will be returned as the response when the object is serialized.
        """
        return OrderSerializer(instance, context=self.context).data
