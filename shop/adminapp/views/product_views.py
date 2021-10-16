from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView
from mainapp.models import Product, ProductCategories, ImageProduct

from adminapp.forms import ProductEditForm
from adminapp.forms import ImageProductForm


def pagination_sample(request, obj, amount):
    paginator = Paginator(obj, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка'
    category = get_object_or_404(ProductCategories, pk=pk)
    product_list = Product.objects.filter(category__pk=pk).order_by('-id')
    pages = pagination_sample(request, product_list, 5)
    img_poster = []
    if list(pages.object_list) != []:
        lst_id_product = []
        for el in pages:
            lst_id_product.append(int(el.id))
        img_poster = ImageProduct.objects.order_by('-id').filter(
            product_id__lte=lst_id_product[0],
            product__gte=lst_id_product[-1]
        ).values()
        img_poster = {el['product_id']: el for el in img_poster}.values()

    content = {
        'title': title,
        'category': category,
        'products': pages,
        'img_product': img_poster,
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategories, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        myfile = request.FILES.getlist('myfile')
        if product_form.is_valid():
            id_product = product_form.save().pk
            product = Product.objects.get(pk=id_product)
            if myfile:
                for f in myfile:
                    fl = ImageProduct(product=product, img_product=f)
                    fl.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title,
               'update_form': product_form,
               'category': category,
               }

    return render(request, 'adminapp/product_update.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product}
#
#     return render(request, 'adminapp/product_read.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['img'] = ImageProduct.objects.filter(product_id=self.get_object().id)[:1].get()
        except:
            context['img'] = []
        return context


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title,
               'update_form': edit_form,
               'category': edit_product.category
               }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.id]))

    content = {'title': title, 'product_to_delete': product}

    return render(request, 'adminapp/product_delete.html', content)
