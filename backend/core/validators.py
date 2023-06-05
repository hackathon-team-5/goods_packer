from typing import OrderedDict

from rest_framework.serializers import ValidationError


def field_validator(obj: OrderedDict,
                    field_list: list) -> None | ValidationError:
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
            raise ValidationError(
                {field: ['Обязательное поле.']}
            )
