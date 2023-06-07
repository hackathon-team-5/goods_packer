from core.models import Create, CreateUpdate
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

User = get_user_model()


class Carton(models.Model):
    cartontype = models.CharField(
        _('идентификатор (код) упаковки'),
        max_length=7,
        unique=True,
    )
    length = models.FloatField(
        _('длина'),
        default=0,
    )
    width = models.FloatField(
        _('ширина'),
        default=0,
    )
    height = models.FloatField(
        _('высота'),
        default=0,
    )
    displayrfpack = models.BooleanField(
        _('коробка есть на складе'),
        default=False,
    )

    class Meta:
        verbose_name = _('характеристика упаковок')
        verbose_name_plural = _('характеристики упаковок')

    def __str__(self):
        return f'{self.cartontype}'


class CargotypeInfo(models.Model):
    cargotype = models.IntegerField(
        _('карготип'),
        unique=True,
    )
    description = models.TextField(
        _('описание карготипа'),
    )

    class Meta:
        verbose_name = _('описание карготипа')
        verbose_name_plural = _('описание карготипов')

    def __str__(self):
        return f'{self.cargotype}'


class CartonPrice(CreateUpdate):
    carton = models.ForeignKey(
        Carton,
        on_delete=models.CASCADE,
        related_name='carton_prices'
    )
    price = models.FloatField(
        _('стоимость'),
        default=0,
    )

    class Meta:
        verbose_name = _('стоимость упаковки')
        verbose_name_plural = _('стоимость упаковок')

    def __str__(self):
        return f'{self.carton} - {self.cost}'


class Sku(Create):
    sku = models.CharField(
        _('название товара'),
        max_length=256,
        unique=True,
    )
    length = models.FloatField(
        _('длина'),
        default=0,
    )
    width = models.FloatField(
        _('ширина'),
        default=0,
    )
    height = models.FloatField(
        _('высота'),
        default=0,
    )
    goods_wght = models.FloatField(
        _('вес'),
        default=0,
    )
    image = ImageField(
        verbose_name=_('Картинка'),
        upload_to='sku_images/',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_('описание'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')

    def __str__(self):
        return f'{self.sku}'


class SkuCargotypes(models.Model):
    objects = None
    sku = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='sku_cargotypes'
    )
    cargotype = models.ForeignKey(
        CargotypeInfo,
        on_delete=models.CASCADE,
        related_name='sku_cargotypes'
    )

    class Meta:
        verbose_name = _('карготип товара')
        verbose_name_plural = _('карготип товаров')
        constraints = (
            models.UniqueConstraint(
                fields=('sku', 'cargotype'),
                name='%(app_label)s_%(class)s_sku_cargotypes_unique',
            ),
        )


class Order(Create):
    whs = models.IntegerField(
        _('код сортировочного центра'),
    )
    orderkey = models.CharField(
        _('id заказа'),
        max_length=32,
    )
    selected_cartontype = models.ForeignKey(
        Carton,
        on_delete=models.CASCADE,
        related_name='orders_selected_cartontype',
        verbose_name=_('код упаковки, которая была выбрана пользователем'),
    )
    box_num = models.IntegerField(
        _('количество коробок'),
    )
    recommended_cartontype = models.ForeignKey(
        Carton,
        on_delete=models.CASCADE,
        related_name='orders_recommended_cartontype',
        verbose_name=_('код упаковки, рекомендованной алгоритмом'),
    )
    sel_calc_cube = models.IntegerField(
        _('объём выбранной упаковки'),
    )
    pack_volume = models.IntegerField(
        _('рассчитанный объём упакованных товаров'),
    )
    rec_calc_cube = models.IntegerField(
        _('(?)'),
    )
    goods_wght = models.FloatField(
        _('вес товара'),
    )
    sku = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    who = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('упаковщик'),
    )
    trackingid = models.CharField(
        _('id доставки'),
        max_length=32,
    )

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    def __str__(self):
        return f'{self.orderkey}'
