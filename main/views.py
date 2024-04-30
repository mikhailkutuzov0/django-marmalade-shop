from django.shortcuts import render
from django.views import View


class IndexView(View):
    """
    Представление главной страницы сайта.

    Обрабатывает GET запросы на главную страницу.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        context = {
            'title': 'Home - Главная',
            'content': 'marmalade-shop-Главная',
        }
        return render(request, 'main/index.html', context)


class AboutView(View):
    """
    Представление страницы 'О нас'.

    Обрабатывает GET запросы на страницу 'О нас'.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        context = {
            'title': 'Marmalade-shop - О нас',
            'content': 'О нас',
            'text_on_page': 'Текст о том что это за магазин'
        }
        return render(request, 'main/about.html', context)


class ContactsView(View):
    """
    Представление страницы контактов.

    Обрабатывает GET запросы на страницу контактов.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        return render(request, 'main/contacts.html')


class DeliveryView(View):
    """
    Представление страницы доставки.

    Обрабатывает GET запросы на страницу доставки.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        return render(request, 'main/delivery.html')
