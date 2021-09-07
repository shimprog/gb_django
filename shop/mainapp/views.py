import json
import os

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, ImageProduct, ProductCategories


def index(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def pagination_sample(request, obj, amount):
    paginator = Paginator(obj, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def products(request, pk=None):
    category = ProductCategories.objects.all()
    if pk == None or pk == 1:
        products_all = Product.objects.order_by('-id').all()
    else:
        products_all = Product.objects.filter(category=int(pk)).order_by('-id').all()
    pages = pagination_sample(request, products_all, 5)
    lst_id_product = []
    for el in pages:
        lst_id_product.append(int(el.id))
    # Одна картинка на продукт
    img_poster = ImageProduct.objects.order_by('-id').filter(
        product_id__lte=lst_id_product[0],
        product__gte=lst_id_product[-1]
    ).values()
    img_poster = {el['product_id']: el for el in img_poster}.values()
    # Все картинки продукта на страницу
    img_full = ImageProduct.objects.filter(product_id__lte=lst_id_product[0], product__gte=lst_id_product[-1])
    content = {'products': pages,
               'img_product': img_poster,
               'img_full': img_full,
               'category': category,
               }
    return render(request, 'mainapp/products.html', content)


def page_not_found_view(request, exception):
    return render(request, 'mainapp/404.html', status=404)