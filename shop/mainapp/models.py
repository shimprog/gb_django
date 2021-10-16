from django.db import models


class ProductCategories(models.Model):
    name = models.CharField('Имя категории', max_length=50, unique=True)
    discriptions = models.TextField(verbose_name="Описание", blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

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
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='категория активна', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def one_img(self):
        return ImageProduct.objects.filter(product_id=self.id)[:1].get()

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class ImageProduct(models.Model):
    img_product = models.FileField(upload_to='product_images', blank=True, null=True, verbose_name='Файл')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.img_product.name

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'




