from rest_framework import serializers
from typing import OrderedDict
from .models import (CargotypeInfo, Carton, CartonPrice, Order, Sku,
                     SkuCargotypes, SkuInWhs, Whs)


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


class OrderSerializer(serializers.ModelSerializer):
    sku = SkuSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'whs',
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

    def validate_sku(self, value):
        for item in value:
            sku = item['sku']
            count = item['count']
            try:
                sku_obj = Sku.objects.get(sku=sku)
                if count > sku_obj.in_stock.count:
                    raise serializers.ValidationError(
                        f"Insufficient stock for SKU: {sku}"
                    )
            except Sku.DoesNotExist:
                raise serializers.ValidationError(f"SKU not found: {sku}")
        return value

    def create(self, validated_data):
        sku_data = validated_data.pop('sku')
        order = Order.objects.create(**validated_data)
        for item in sku_data:
            sku = item['sku']['sku']
            count = item['count']
            order.sku.add(
                Sku.objects.get(sku=sku), through_defaults={'count': count}
            )
        return order
