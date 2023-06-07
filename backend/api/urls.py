from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import CartonViewSet, CargotypeInfoViewSet, CartonPriceViewSet, \
    SkuViewSet, SkuCargotypesViewSet, OrderViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Goods packer",
      default_version='v1',
      description="Project for hackathon from team #5",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'carton', CartonViewSet, basename='cartons')
router.register('cargo_type_info', CargotypeInfoViewSet, basename='cargo_types_info')
router.register('carton_price', CartonPriceViewSet, basename='carton_prices')
router.register('sku', SkuViewSet, basename='skus')
router.register('sku_cargo_type', SkuCargotypesViewSet, basename='sku_cargo_types')
router.register('order', OrderViewSet, basename='Orders')


urlpatterns = [
    path('', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
