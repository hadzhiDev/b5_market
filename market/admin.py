# # from ckeditor_uploader.widgets import CKEditorUploadingWidget
# # from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from market.models import Tag, Category, Product, ProductImage, ProductAttribute


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


# # class ProductAdminForm(forms.ModelForm):

# #     content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')
# #     description = forms.CharField(widget=forms.Textarea, label='Описание', help_text='Просто описание')

# #     class Meta:
# #         model = Product
# #         fields = '__all__'


class ProductImageStackedInline(admin.TabularInline):

    model = ProductImage
    extra = 1


class ProductAttributeStackedInline(admin.TabularInline):

    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_filter = ('category', 'tags', 'is_published',)
    search_fields = ('name', 'description', 'content',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    # form = ProductAdminForm
    inlines = [ProductAttributeStackedInline, ProductImageStackedInline]

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="150px">')
        return '-'

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'
