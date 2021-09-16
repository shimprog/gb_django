from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string

from .models import Basket
from mainapp.models import Product, ImageProduct


@login_required
def basket(request):
    title = 'Корзина'
    basket = Basket.objects.filter(user=request.user).all()
    img_poster = []
    lst_id_product = []
    for el in basket.values():
        lst_id_product.append(int(el['product_id']))

    if lst_id_product != []:
        img_poster = ImageProduct.objects.order_by('-id').filter(
            product_id__lte=lst_id_product[0],
            product__gte=lst_id_product[-1]
        ).values()
        img_poster = {el['product_id']: el for el in img_poster}.values()

    content = {
        'img_poster': img_poster,
        'title': title,
        'basket': basket,
    }
    return render(request, 'basket/base.html', content)


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(product_id=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).all()
        img_poster = []
        lst_id_product = []
        for el in basket_items.values():
            lst_id_product.append(int(el['product_id']))

        if lst_id_product != []:
            img_poster = ImageProduct.objects.order_by('-id').filter(
                product_id__lte=lst_id_product[0],
                product__gte=lst_id_product[-1]
            ).values()
            img_poster = {el['product_id']: el for el in img_poster}.values()

        content = {
            'basket': basket_items,
            'img_poster': img_poster,
        }

        result = render_to_string('basket/basket.html', content)

        return JsonResponse({'result': result})


@login_required
def basket_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

