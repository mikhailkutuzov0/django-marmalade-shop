from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home - Главная',
        'content': 'marmelade-shop',
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Marmalade-shop - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том что это за магазин '
    }
    return render(request, 'main/about.html', context)
