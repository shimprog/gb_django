from django.db import models


class ProductCategories(models.Model):
    name = models.CharField('Имя категории', max_length=50, unique=True)
    discriptions = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Имя товара', max_length=50)
    discriptions = models.TextField(verbose_name="Описание", blank=True)
    price = models.CharField('Цена товара', max_length=20)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ImageProduct(models.Model):
    img_product = models.ImageField('Изображение', upload_to="product_images", blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.img_product.name

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'




