import os

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from order.logic import create_stripe_checkout_session, add_item_in_cart, sub_item_in_cart, cart_items_info, \
    filter_cart_with_currency, create_order_from_cart, pay_form_order
from order.models import Order


class BuyItemView(View):
    """
    Buy Item
    p.s. Решил оставит для основных пунктов задачи )
    """
    def get(self, request, pk):
        session = create_stripe_checkout_session([{'id': pk, 'quantity': 1}], promos=[])
        return JsonResponse({
            'session': {
                'id': session.id,
                'url': session.url
            }
        })


class AddItemToCart(View):
    """Add item to cart"""
    def get(self, request, pk):
        request.session['cart'] = add_item_in_cart(request.session.get('cart', False), pk)
        return JsonResponse({
            'status': 'Ok',
            'cart': cart_items_info(request.session['cart']),
        })


class SubItemFromCart(View):
    """Remove item from cart"""
    def get(self, request, pk):
        request.session['cart'] = sub_item_in_cart(request.session['cart'], pk)
        return JsonResponse({
            'status': 'Ok',
            'cart': cart_items_info(request.session['cart']),
        })


class CreateOrderFromCart(View):
    """Create Order from cart for one currency"""
    def get(self, request, currency):
        _cart = request.session.get('cart', {})
        cart = cart_items_info(request.session.get('cart', {}))
        filtered_cart = filter_cart_with_currency(cart, currency)
        order = create_order_from_cart(filtered_cart, request.session.get('promos', {}))
        for cart_item in cart:
            if cart_item['currency'] == currency:
                del _cart[str(cart_item['id'])]
        request.session['cart'] = _cart
        return redirect(reverse('order_detail', kwargs={'pk': order.id}))


class OrderDetail(DetailView):
    """Order detail with all information - items, discounts"""
    model = Order
    template_name = 'order/detail.html'
    queryset = Order.objects.prefetch_related(
        'order_items',
        'order_items__item',
        'discount_bundles',
        'discount_bundles__promo',
        'discount_bundles__coupon',
    ).all()

    def get_context_data(self, **kwargs):
        """Overwritten for sending Stripe Public API Key to front"""
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['API_KEY_PK'] = os.environ.get('API_KEY_PK', f'api_key')
        return context


class PayFromOrder(View):
    """Pay order total is Stripe"""
    def get(self, request, pk):
        session = pay_form_order(pk)
        return JsonResponse({
            'session': {
                'id': session.id,
                'url': session.url
            }
        })


class OrderListView(ListView):
    """Page for orders"""
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 100
