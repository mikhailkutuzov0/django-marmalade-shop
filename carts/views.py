from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from carts.models import Cart
from goods.models import Products
from carts.utils import get_user_carts


class CartAddView(View):
    """
    Представление для добавления товара в корзину.

    Обрабатывает POST-запросы для добавления товаров в корзину пользователя,
    автоматически увеличивает количество если товар уже есть в корзине.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)
        if request.user.is_authenticated:
            # Создание элемента корзины для аутентифицированного пользователя
            cart, created = Cart.objects.get_or_create(
                user=request.user, product=product)
            if not created:
                cart.quantity += 1
                cart.save()
        else:
            # Создание элемента корзины для неаутентифицированного пользователя
            cart, created = Cart.objects.get_or_create(
                session_key=request.session.session_key, product=product)
            if not created:
                cart.quantity += 1
                cart.save()

        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html",
            {"carts": user_cart},
            request=request
        )

        return JsonResponse({
            "message": "Товар добавлен в корзину",
            "cart_items_html": cart_items_html,
        })


class CartChangeView(View):
    """
    Представление для изменения количества товара в корзине.

    Обрабатывает POST-запросы для изменения количества товара в корзине,
    сохраняя изменения в базе данных.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()

        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html",
            {"carts": user_cart},
            request=request
        )

        return JsonResponse({
            "message": "Количество изменено",
            "cart_items_html": cart_items_html,
            "quantity": cart.quantity,
        })


class CartRemoveView(View):
    """
    Представление для удаления товара из корзины.

    Обрабатывает POST-запросы для удаления товара из корзины пользователя и
    обновляет отображаемую информацию о корзине.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        quantity = cart.quantity
        cart.delete()

        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html",
            {"carts": user_cart},
            request=request
        )

        return JsonResponse({
            "message": "Товар удален",
            "cart_items_html": cart_items_html,
            "quantity_deleted": quantity,
        })
