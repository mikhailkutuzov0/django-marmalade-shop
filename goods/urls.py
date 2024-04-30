from django.urls import path
from . import views

app_name = 'catalog'  # Пространство имен для URL-адресов

urlpatterns = [
    # Страница поиска в каталоге
    path('search/', views.CatalogView.as_view(), name='search'),
    # Страница каталога по категориям
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    # Страница конкретного продукта
    path('product/<slug:product_slug>/',
         views.ProductView.as_view(), name='product'),
]
