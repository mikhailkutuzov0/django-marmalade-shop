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
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name, {
            'title': 'marlmelade-shop - Авторизация',
            'form': self.form_class()
        })

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(
                    request, f'{username}, вы успешно вошли в аккаунт')
                if session_key:
                    Cart.objects.filter(
                        session_key=session_key).update(user=user)
                return HttpResponseRedirect(
                    request.POST.get('next', reverse('main:index'))
                )
        return render(
            request, self.template_name,
            {
                'form': form,
                'title': 'marlmelade-shop - Авторизация'
            }
        )


class RegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    def get(self, request):
        return render(request, self.template_name, {
            'title': 'marlmelade-shop - Регистрация',
            'form': self.form_class()
        })

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            session_key = request.session.session_key
            auth.login(request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(
                request,
                f'{user.username}, вы зарегестрировались и вошли в аккаунт'
            )
            return HttpResponseRedirect(reverse('main:index'))
        return render(
            request,
            self.template_name,
            {'form': form, 'title': 'marlmelade-shop - Регистрация'}
        )


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get(self, request):
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
        form = self.form_class(
            data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профайл успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
        return render(
            request,
            self.template_name,
            {'form': form, 'title': 'Home - Кабинет'}
        )


class UsersCartView(View):
    def get(self, request):
        return render(request, 'users/users_cart.html')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        messages.success(request, "Вы вышли из аккаунта")
        auth.logout(request)
        return redirect(reverse('main:index'))
