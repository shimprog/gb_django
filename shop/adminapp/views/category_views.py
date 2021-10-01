from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from mainapp.models import ProductCategories
from adminapp.forms import ProductCategoryEditForm
from adminapp.views.user_views import AdminPanelProtectionMixin


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'Категории'
#
#     category_list = ProductCategories.objects.all()
#     content = {
#         'title': title,
#         'object_list': category_list
#     }
#     return render(request, 'adminapp/categories.html', content)


class ProductCategoryListView(AdminPanelProtectionMixin, ListView):
    model = ProductCategories
    template_name = 'adminapp/categories.html'

    def get(self, request, *args, **kwargs):
        if 'X-Requested-With' in request.headers:
            self.template_name = 'adminapp/categories_ajax.html'
            old_render = super().get(request, *args, **kwargs)
            new_render = old_render.rendered_content
            return JsonResponse({'data': new_render})
        else:
            return super().get(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'Создание категории'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/user_update.html', content)


class ProductCategoryCreateView(AdminPanelProtectionMixin, CreateView):
    model = ProductCategories
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'Редактирование категории'
#
#     category = get_object_or_404(ProductCategories, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, instance=category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=category)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)


class ProductCategoryUpdateView(AdminPanelProtectionMixin, UpdateView):
    model = ProductCategories
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategories, pk=pk)
#
#     if request.method == 'POST':
#         category.delete()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'adminapp/category_delete.html', content)


class ProductCategoryDeleteView(AdminPanelProtectionMixin, DeleteView):
    model = ProductCategories
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())