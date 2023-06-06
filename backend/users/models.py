from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        CHIEF = 'chief', _('старший смены')
        USER = 'user', _('упаковщик')

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(3)]
    )
    who = models.CharField(
        _('id упаковщика'),
        null=True,
        blank=True,
        max_length=32,
    )
    role = models.CharField(
        verbose_name=_('Пользовательская роль'),
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
