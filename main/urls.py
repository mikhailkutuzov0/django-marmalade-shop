from django.urls import path
from . import views

app_name = 'main'  # Пространство имен для URL-адресов

urlpatterns = [
    # Главная страница:
    path('', views.IndexView.as_view(), name='index'),
    # Страница "О нас"
    path('about/', views.AboutView.as_view(), name='about'),
    # Страница контактов
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    # Страница с информацией о доставке
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
]
