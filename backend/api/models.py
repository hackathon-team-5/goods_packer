from core.models import Create, CreateUpdate
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

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

        constraints = (
            models.UniqueConstraint(
                fields=('carton',),
                name='%(app_label)s_%(class)s_carton_unique',
            ),
        )

    def __str__(self):
        return f'{self.carton} - {self.price}'


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
    image = models.CharField(
        _('URL на картинку'),
        max_length=256,
    )
    description = models.TextField(
        _('описание'),
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


class Whs(models.Model):
    whs = models.CharField(
        _('название сортировочного центра'),
        max_length=256,
        unique=True,
    )

    class Meta:
        verbose_name = _('количество товара на складе')
        verbose_name_plural = _('количество товаров на складе')


class SkuInWhs(CreateUpdate):
    sku = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='in_stock'

    )
    whs = models.ForeignKey(
        Whs,
        on_delete=models.CASCADE,
        related_name='in_stock',
    )
    amount = models.BigIntegerField(
        _('количество'),
    )

    class Meta:
        verbose_name = _('количество товара на складе')
        verbose_name_plural = _('количество товаров на складе')
        constraints = (
            models.UniqueConstraint(
                fields=('sku', 'whs'),
                name='%(app_label)s_%(class)s_sku_whs_unique',
            ),
        )


class Order(CreateUpdate):
    class Status(models.TextChoices):
        FORMED = 'formed', _('Формируется')
        COLLECTED = 'collected', _('Собирается')
        READY = 'ready', _('Готов')

    whs = models.ForeignKey(
        Whs,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('код сортировочного центра'),
    )
    orderkey = models.CharField(
        _('id заказа'),
        max_length=32,
    )
    box_num = models.IntegerField(
        _('количество коробок'),
        default=0,
    )
    sel_calc_cube = models.IntegerField(
        _('объём выбранной упаковки'),
        default=0,
    )
    pack_volume = models.IntegerField(
        _('рассчитанный объём упакованных товаров'),
        default=0,
    )
    rec_calc_cube = models.IntegerField(
        _('(?)'),
        null=True,
        blank=True,
    )
    goods_wght = models.FloatField(
        _('вес товара'),
        default=0,
    )
    sku = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True,
    )
    who = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('упаковщик'),
        null=True,
        blank=True,
    )
    trackingid = models.CharField(
        _('id доставки'),
        max_length=32,
        blank=True,
    )
    status = models.CharField(
        _('Статус'),
        max_length=9,
        choices=Status.choices,
        default=Status.FORMED
    )

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    def __str__(self):
        return f'{self.orderkey}'


class SkuInOrder(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name=_('Ордер'),
        related_name='qt_skus',
        on_delete=models.CASCADE,
    )
    sku = models.ForeignKey(
        Sku,
        verbose_name=_('SKU'),
        related_name='qt_orders',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        _('Количество'),
        default=0,
    )
    recommended_cartontype = models.ForeignKey(
        Carton,
        on_delete=models.CASCADE,
        related_name='orders_sku_recommended_cartontype',
        verbose_name=_('код упаковки, рекомендованной алгоритмом'),
        null=True,
        blank=True,
    )
    selected_cartontype = models.ForeignKey(
        Carton,
        on_delete=models.CASCADE,
        related_name='orders_sku_selected_cartontype',
        verbose_name=_('код упаковки, которая была выбрана пользователем'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Sku in Order'
        verbose_name_plural = 'Sku in Orders'
        ordering = ('order', )

    def __str__(self) -> str:
        return f'{self.order} {self.sku} {self.amount}'
