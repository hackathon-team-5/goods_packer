from typing import OrderedDict

from api.models import Sku
from rest_framework import serializers


def field_validator(obj: OrderedDict,
                    field_list: list) -> None | serializers.ValidationError:
    """
    This is a function that takes in two parameters, an ordered dictionary
    object and a list of fields. The purpose of this function is to validate
    whether the given fields in the object are not empty or null. If any of
    the fields are empty or null, a "ValidationError" is raised with a message
    stating that the field is mandatory.
    """

    for field in field_list:
        check = obj.get(field)
        if not check or check == '':
            raise serializers.ValidationError(
                {field: ['Обязательное поле.']}
            )


def sku_validator(self, list_sku: list) -> list | serializers.ValidationError:
    """
    The function "sku_validator" takes in two parameters: "self", and a list
    of product SKUs and their respective amounts.

    The function iterates through each item in the list of SKUs and amounts.
    For each item, the sku and count are extracted.

    Then the function tries to retrieve an instance of the Sku model using the
    sku. If the Sku is found, the function checks if there is enough stock by
    retrieving the first in_stock object, and comparing its amount to the
    count. If there is insufficient stock, an error is raised.

    If the Sku does not exist, an error is raised.

    Finally, the function returns the list of SKUs and amounts.
    """
    for item in list_sku:
        sku = item['sku']
        count = item['amount']
        try:
            sku_obj = Sku.objects.get(sku=sku)
            sku_in_whs = sku_obj.in_stock.first()
            if count > sku_in_whs.amount:
                raise serializers.ValidationError(
                    f'Insufficient stock for SKU: {sku}'
                )
        except Sku.DoesNotExist:
            raise serializers.ValidationError(f'SKU not found: {sku}')
    return list_sku
