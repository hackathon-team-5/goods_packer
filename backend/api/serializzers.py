from rest_framework import serializers

from .models import Carton, CargotypeInfo, CartonPrice, Sku, SkuCargotypes, Order


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

    class Meta:
        model = Sku
        fields = (
            'sku',
            'a',
            'b',
            'c',
            'weight',
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
            'trackingid'
        )
