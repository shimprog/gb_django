import json
import os
import datetime
from django.core.management.base import BaseCommand
from mainapp.models import Product, ProductCategories, ImageProduct
from requests import get


class Command(BaseCommand):
    def unpacking_product(self, **kwargs):
        z = ''
        for el, el2 in kwargs.items():
            z += f'{el}: {el2} \n'
        return z

    def add_arguments(self, parser):
        parser.add_argument('param', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        options
        1. id таблицы, 2. mainapp\имя json
        пример: 1 mebel_office.json
        """
        # Product.objects.all().delete()
        # ImageProduct.objects.all().delete()
        category = ProductCategories.objects.get(pk=options['param'][0])
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        os.makedirs(f'./media/{str(category)}/{current_date}/')

        with open(f"mainapp\{options['param'][1]}", encoding='utf-8') as read_json:
            data = json.load(read_json)

        for el in data:
            try:
                price = el['price']
            except KeyError:
                price = 0
            new_product = Product(
                category=category,
                name=el['name'],
                price=price,
                discriptions=self.unpacking_product(**el['specifications']))
            new_product.save()
            i = 0
            for img in el['photos']:
                img = f'https://{img[2:]}'
                url = get(img)
                with open(f'media/{str(category)}/{current_date}/{new_product.id}-{i}.jpg', 'wb') as f:
                    f.write(url.content)
                new_img = ImageProduct(
                    img_product=f'{str(category)}/{current_date}/{new_product.id}-{i}.jpg',
                    product=new_product)
                new_img.save()
                i += 1
        print('ok')
        return 'ya'
