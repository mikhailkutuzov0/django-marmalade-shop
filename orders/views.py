from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@method_decorator(login_required, name='dispatch')
class CreateOrderView(View):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm

    def get(self, request, *args, **kwargs):
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = self.form_class(initial=initial)
        context = {
            'title': 'Marmalade-shop - Оформление заказа',
            'form': form,
            'orders': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = self.create_order(user, form, cart_items)
                        cart_items.delete()
                        messages.success(request, 'Заказ оформлен.')
                        return redirect('users:profile')
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('cart:order')
        return render(request, self.template_name, {'form': form})

    def create_order(self, user, form, cart_items):
        order = Order.objects.create(
            user=user,
            phone_number=form.cleaned_data['phone_number'],
            requires_delivery=form.cleaned_data['requires_delivery'],
            delivery_address=form.cleaned_data['delivery_address'],
            payment_on_get=form.cleaned_data['payment_on_get'],
        )
        for cart_item in cart_items:
            product = cart_item.product
            name = product.name
            price = product.discounted_price()
            quantity = cart_item.quantity

            if product.quantity < quantity:
                raise ValidationError(
                    f'На складе недостаточно {name} В наличии - {product.quantity}'
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                name=name,
                price=price,
                quantity=quantity,
            )
            product.quantity -= quantity
            product.save()
        return order
