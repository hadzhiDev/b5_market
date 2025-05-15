from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny, IsAdminUser, 
                                        IsAuthenticatedOrReadOnly, 
                                        IsAuthenticated)

from market.models import Tag, Category, Product, ProductImage, ProductAttribute
from market.serializers import TagSerializer, CategorySerializer, ProductSerializer, ProductImageSerializer, \
    ProductAttributeSerializer
from market.permissions import IsOwnerORSuperUser


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerORSuperUser]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductAttributeViewSet(ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer