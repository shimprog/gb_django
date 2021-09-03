import json
import os

from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def pagination_sample(request, obj, amount):
    paginator = Paginator(obj, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def products(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    # print(os.getcwd())
    with open("mainapp\mebel_office.json", encoding='utf-8') as read_json:
        data = json.load(read_json)

    pages = pagination_sample(request, data, 5)
    content = {'links': links_menu, 'json_product': pages}
    return render(request, 'mainapp/products.html', content)


def page_not_found_view(request, exception):
    return render(request, 'mainapp/404.html', status=404)