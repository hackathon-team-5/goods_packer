from typing import OrderedDict

from core.utils import key_generator
from core.validators import field_validator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (CharField, ModelSerializer, Serializer,
                                        ValidationError)

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Serializer to work with the User model.
    """
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'who',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate(self, obj: OrderedDict) -> OrderedDict:
        """
        Validating fields.
        """
        field_list = [
            'username', 'first_name', 'last_name', 'password'
        ]
        field_validator(obj, field_list)
        return obj


class SetPasswordSerializer(Serializer):
    """Change the password of the current user."""
    new_password = CharField()
    current_password = CharField()

    class Meta:
        model = User
        fields = (
            'new_password',
            'current_password',
        )
        extra_kwargs = {
            'new_password': {'required': True, 'allow_blank': False},
            'current_password': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        """
        Validating new password.
        """
        validate_password(obj['new_password'])
        return super().validate(obj)

    def update(self, instance, valid_data) -> OrderedDict:
        """
        Saving a new password.
        """
        if not instance.check_password(valid_data['current_password']):
            raise ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if valid_data['current_password'] == valid_data['new_password']:
            raise ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(valid_data['new_password'])
        instance.save()
        return valid_data
