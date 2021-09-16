from django.urls import path
import mainapp.views as views


app_name = 'products'

urlpatterns = [
    path('', views.products, name='product'),
    path('<int:pk>', views.products),
    path('<int:pk>/<int:pk1>', views.product, name='product_full'),
]

