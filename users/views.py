from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Prefetch

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class LoginView(View):
    """
    Представление для авторизации пользователя.

    Обрабатывает GET и POST запросы на странице авторизации. В случае успешной
    авторизации перенаправляет пользователя на главную страницу.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    # Инициализация формы логина и шаблона для отображения
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        """
        Обрабатывает GET запросы и отображает форму авторизации.
        """
        return render(request, self.template_name, {
            'title': 'marlmelade-shop - Авторизация',
            'form': self.form_class()
        })

    def post(self, request):
        """
        Обрабатывает POST запросы, выполняет проверку данных формы и
        авторизует пользователя.
        """
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(
                    request, f'{username}, вы успешно вошли в аккаунт')
                session_key = request.session.session_key
                if session_key:
                    # Обновление корзины при смене сессии
                    Cart.objects.filter(
                        session_key=session_key).update(user=user)
                return HttpResponseRedirect(
                    request.POST.get('next', reverse('main:index'))
                )
        return render(request, self.template_name, {
            'form': form,
            'title': 'marlmelade-shop - Авторизация'
        })


class RegistrationView(View):
    """
    Представление для регистрации пользователя.

    Обрабатывает GET и POST запросы на странице регистрации. После успешной
    регистрации происходит автоматический вход в систему и перенаправление
    на главную страницу.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    def get(self, request):
        """
        Обрабатывает GET запросы и отображает форму регистрации.
        """
        return render(request, self.template_name, {
            'title': 'marlmelade-shop - Регистрация',
            'form': self.form_class()
        })

    def post(self, request):
        """
        Обрабатывает POST запросы, выполняет проверку данных
        формы и регистрирует пользователя.
        """
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            session_key = request.session.session_key
            if session_key:
                # Обновление корзины при смене сессии
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(
                request,
                f'{user.username}, вы зарегистрировались и вошли в аккаунт'
            )
            return HttpResponseRedirect(reverse('main:index'))
        return render(request, self.template_name, {
            'form': form,
            'title': 'marlmelade-shop - Регистрация'
        })


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """
    Представление для отображения и обновления профиля пользователя.

    Обрабатывает GET и POST запросы. GET запросы отображают форму профиля,
    а POST запросы обрабатывают изменения в профиле пользователя.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get(self, request):
        """
        Обрабатывает GET запросы, отображает форму профиля с текущими данными
        пользователя и историей заказов.
        """
        form = self.form_class(instance=request.user)
        orders = Order.objects.filter(user=request.user).prefetch_related(
            Prefetch("orderitem_set",
                     queryset=OrderItem.objects.select_related("product"))
        ).order_by("-id")
        return render(request, self.template_name, {
            'title': 'Home - Кабинет',
            'form': form,
            'orders': orders
        })

    def post(self, request):
        """
        Обрабатывает POST запросы, обновляет данные пользователя исходя
        из формы и сохраняет изменения.
        """
        form = self.form_class(
            data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профайл успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
        return render(request, self.template_name, {
            'form': form,
            'title': 'Home - Кабинет'
        })


class UsersCartView(View):
    """
    Представление корзины пользователя.

    Отображает корзину текущего пользователя, содержащую выбранные им товары.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        return render(request, 'users/users_cart.html')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """
    Представление для выхода пользователя из системы.

    Выполняет выход из системы и перенаправляет на главную страницу.

    Args:
        request (HttpRequest): объект запроса от пользователя.
    """

    def get(self, request):
        messages.success(request, "Вы вышли из аккаунта")
        auth.logout(request)
        return redirect(reverse('main:index'))
