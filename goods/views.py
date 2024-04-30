from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.views import View
from goods.models import Products
from goods.utils import q_search


class CatalogView(View):
    """
    Представление для отображения списка товаров в каталоге.

    Отображает товары по категории или поисковому запросу с возможностью
    сортировки и фильтрации.

    Args:
        request (HttpRequest): объект запроса от пользователя.
        category_slug (str, optional): слаг категории товаров для фильтрации,
                                       или 'all' для показа всех товаров.
    """

    def get(self, request, category_slug=None):
        # Получение параметров из запроса
        page = request.GET.get('page', 1)
        on_sale = request.GET.get('on_sale', None)
        order_by = request.GET.get('order_by', None)
        query = request.GET.get('q', None)

        # Фильтрация товаров в зависимости от категории или поискового запроса
        if category_slug == 'all':
            goods = Products.objects.all()  # Получение всех товаров,если 'all'
        elif query:
            goods = q_search(query)  # Поиск товаров по заданному запросу
        else:
            # Получение товаров по слагу или 404, если ничего не найдено
            goods = get_list_or_404(
                Products.objects.filter(category__slug=category_slug))

        # Применение фильтров и сортировки
        if on_sale:
            goods = goods.filter(discount__gt=0)  # Товары со скидкой
        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)  # Сортировка товаров

        # Пагинация
        # Создание пагинатора для товаров, по 9 на страницу
        paginator = Paginator(goods, 9)
        current_page = paginator.page(int(page))  # Получение текущей страницы

        context = {
            "title": "Каталог",
            "goods": current_page,
            'slug_url': category_slug
        }
        return render(request, "goods/catalog.html", context)


class ProductView(View):
    """
    Представление для отображения деталей продукта.

    Показывает подробную информацию о конкретном товаре.

    Args:
        request (HttpRequest): объект запроса от пользователя.
        product_slug (str): слаг продукта для отображения.
    """

    def get(self, request, product_slug):
        # Получение продукта по слагу или возврат 404, если продукт не найден
        product = Products.objects.get(slug=product_slug)
        context = {
            'product': product
        }
        return render(request, "goods/product.html", context)
