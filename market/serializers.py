from rest_framework.serializers import ModelSerializer

from accounts.models import User
from market.models import Tag, Category, Product, ProductImage, ProductAttribute


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class CategoryForProductReadSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagForProductReadSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class UserForProductReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'avatar')


class ProductAttributeForProductReadSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'value')


class ProductImageForProductReadSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(ModelSerializer):
    category = CategoryForProductReadSerializer(many=False)
    tags = TagForProductReadSerializer(many=True)
    owner = UserForProductReadSerializer(many=False)
    attributes = ProductAttributeForProductReadSerializer(many=True)
    images = ProductImageForProductReadSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'