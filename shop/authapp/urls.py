from django.urls import path, re_path
import authapp.views as authview

app_name = 'authapp'

urlpatterns = [
    path('login/', authview.login, name='login'),
    path('logout/', authview.logout, name='logout'),
    path('register/', authview.register, name='register'),
    path('edit/', authview.edit, name='edit'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authview.verify, name='verify'),
]