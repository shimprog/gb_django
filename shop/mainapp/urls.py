from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('contacts', views.contact, name='contacts'),
    path('products', views.products, name='products'),
]

