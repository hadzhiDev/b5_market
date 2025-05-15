from django.urls import path, include

from rest_framework.routers import DefaultRouter

from market import views
from .yasg import urlpatterns as yasg_urlpatterns

router = DefaultRouter()

router.register('tags', views.TagViewSet)
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('product-images', views.ProductImageViewSet)
router.register('product-attributes', views.ProductAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.auth.urls'))
]

urlpatterns += yasg_urlpatterns


