"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mainapp import views as mainapp_v


urlpatterns = [
    path('', mainapp_v.index, name='home'),
    path('contacts', mainapp_v.contact, name='contacts'),
    # path('admin/', admin.site.urls),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('orderapp.urls', namespace='order')),
]

if settings.DEBUG:
    urlpatterns += (
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

# При отключенном дебаге будет работать
handler404 = "mainapp.views.page_not_found_view"