from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategories


def pagination_sample(request, obj, amount):
    paginator = Paginator(obj, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def products(request, pk):
    title = 'админка'
    category = get_object_or_404(ProductCategories, pk=pk)
    product_list = Product.objects.filter(category__pk=pk).order_by('name')
    pages = pagination_sample(request, product_list, 5)
    content = {
        'title': title,
        'category': category,
        'products': pages
    }
    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass