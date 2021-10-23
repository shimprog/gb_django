import random

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .models import Product, ImageProduct, ProductCategories
from basket.models import Basket


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategories.objects.filter(is_active=True)
            cache.set(key, links_menu)
            return links_menu
    else:
        return ProductCategories.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategories, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategories, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def index(request):
    products = get_products()[:3]
    content = {'products': products}
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {}
    return render(request, 'mainapp/contact.html', content)


def pagination_sample(request, obj, amount):
    paginator = Paginator(obj, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@cache_page(3600)
def products(request, pk=None):
    category = ProductCategories.objects.all()
    # category = get_category(pk)
    if pk is None:
        # products_all = Product.objects.order_by('-id').all()
        products_all = get_products()
    else:
        # products_all = Product.objects.filter(category=int(pk)).order_by('-id').all()
        products_all = get_products_in_category_orederd_by_price(pk)
    pages = pagination_sample(request, products_all, 5)
    img_poster = []
    img_full = []
    if list(pages.object_list):
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


def product(request, pk=None, pk1=None):
    # product = Product.objects.get(id=pk1)
    product = get_product(pk1)
    img_full = ImageProduct.objects.filter(product_id=pk1).all()
    content = {
        'product': product,
        'img_full': img_full,
    }
    return render(request, 'mainapp/product.html', content)


def page_not_found_view(request, exception):
    return render(request, 'mainapp/404.html', status=404)
