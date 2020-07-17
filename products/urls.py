from django.urls import path, include
from .views import *
from .models import Roaster

app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('filter', search, name='search'),
    path('create/', product_create_view, name='product-list'),
    path('<int:id>/', product_detail_view, name='product-detail'),
    path('<int:id>/update/', product_update_view, name='product-update'),
    path('<int:id>/delete/', product_delete_view, name='product-delete'),
]