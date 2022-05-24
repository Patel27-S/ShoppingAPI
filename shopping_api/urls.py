from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from shoping_api_app import views, api_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<int:id>/', views.show, name='show-product'),
    path('cart/', views.cart, name='shopping-cart'),
    path('', views.index, name='list-products'),
    path('api/v1/products/', api_views.ProductList.as_view(),
         name='listing-all-products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
