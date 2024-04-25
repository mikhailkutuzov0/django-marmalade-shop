from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home - Главная',
        'content': 'marmalade-shop-Главная',
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Marmalade-shop - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том что это за магазин '
    }
    return render(request, 'main/about.html', context)


def contacts(request):
    return render(request, 'main/contacts.html')


def delivery(request):
    return render(request, 'main/delivery.html')
