from django.urls import path
from . import views

app_name = 'carts'  # Пространство имен для URL-адресов

urlpatterns = [
    # Добавление товара в корзину
    path('cart_add/', views.CartAddView.as_view(), name='cart_add'),
    # Изменение количества товара в корзине
    path('cart_change/', views.CartChangeView.as_view(), name='cart_change'),
    # Удаление товара из корзины
    path('cart_remove/', views.CartRemoveView.as_view(), name='cart_remove'),
]
