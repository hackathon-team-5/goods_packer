from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from .models import (CargotypeInfo, Carton, CartonPrice, Order, Sku,
                     SkuCargotypes)

User = get_user_model()


class CartonPriceInline(admin.StackedInline):
    model = CartonPrice
    extra = 0


@admin.register(Carton)
class CartonAdmin(admin.ModelAdmin):
    list_display = (
        'cartontype',
    )
    fieldsets = (
        ('Основное', {'fields': ('cartontype', 'displayrfpack')}),
        ('Размеры', {'fields': ('length', 'width', 'height')}),
    )
    empty_value_display = '-пусто-'
    inlines = (CartonPriceInline,)


@admin.register(CargotypeInfo)
class CargotypeInfoAdmin(admin.ModelAdmin):
    list_display = (
        'cargotype',
    )
    empty_value_display = '-пусто-'


class SkuCargotypesInline(admin.StackedInline):
    model = SkuCargotypes
    extra = 0


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
    )
    fieldsets = (
        ('Основное', {'fields': ('sku', 'description')}),
        ('Размеры', {'fields': ('length', 'width', 'height')}),
        ('Картинка', {'fields': ('image', 'preview')}),
    )
    empty_value_display = '-пусто-'
    inlines = (SkuCargotypesInline,)
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'whs', 'orderkey', 'who'
    )
    fieldsets = (
        ('Основное', {'fields': ('sku', 'whs', 'orderkey')}),
        ('Информация об упаковке', {
            'fields': (
                'recommended_cartontype',
                'pack_volume',
                'selected_cartontype',
                'sel_calc_cube',
                'box_num',
                'goods_wght',
                'rec_calc_cube',
            )
        }),
        ('Подготовка к отправке', {'fields': ('who', 'trackingid')}),
    )
    empty_value_display = '-пусто-'
