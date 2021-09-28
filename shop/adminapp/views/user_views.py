from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from authapp.forms import ShopUserRegisterForm
from django.urls import reverse, reverse_lazy
from adminapp.forms import ShopUserAdminEditForm


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка'
#
#     user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     content = {
#         'title': title,
#         'objects': user_list
#     }
#     return render(request, 'adminapp/users.html', content)
class AdminPanelProtectionMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserListView(AdminPanelProtectionMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'form': user_form}
#
#     return render(request, 'adminapp/user_update.html', content)


class UserCreateView(AdminPanelProtectionMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             # return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)


class UserUpdateView(AdminPanelProtectionMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.delete()
#         # вместо удаления лучше сделаем неактивным
#         # user.is_active = False
#         # user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', content)


class UserDeleteView(AdminPanelProtectionMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
