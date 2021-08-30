from django.shortcuts import render


def index(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def products(request):
    return render(request, 'mainapp/products.html')


def page_not_found_view(request, exception):
    return render(request, 'mainapp/404.html', status=404)