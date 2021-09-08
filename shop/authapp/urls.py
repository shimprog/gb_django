from django.urls import path
import authapp.views as authview

app_name = 'authapp'

urlpatterns = [
    path('login/', authview.login, name='login'),
    path('logout/', authview.logout, name='logout'),
    path('register/', authview.register, name='register'),
    path('edit/', authview.edit, name='edit'),
]