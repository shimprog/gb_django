from django.contrib import admin
from .models import ProductCategories, Product, ImageProduct


class ProductImageInline(admin.StackedInline):
  model = ImageProduct


class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImageInline,]


admin.site.register(ProductCategories)
admin.site.register(Product, ProductAdmin)
admin.site.register(ImageProduct)



