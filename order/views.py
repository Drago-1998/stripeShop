from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from order.logic import create_stripe_checkout_session, add_item_in_cart, sub_item_in_cart, cart_items_info


class BuyItemView(View):
    """
    Buy Item with Django Basic View Based

    p.s. Решил оставит для основных пунктов задачи )
    """
    def get(self, request, pk):
        session = create_stripe_checkout_session([pk])
        return JsonResponse({
            'session': {
                'id': session.id,
                'url': session.url
            }
        })


class AddItemToCart(View):

    def get(self, request, pk):
        request.session['cart'] = add_item_in_cart(request.session.get('cart', False), pk)
        return JsonResponse({
            'status': 'Ok',
            'cart': cart_items_info(request.session['cart']),
        })


class SubItemFromCart(View):

    def get(self, request, pk):
        request.session['cart'] = sub_item_in_cart(request.session['cart'], pk)
        return JsonResponse({
            'status': 'Ok',
            'cart': cart_items_info(request.session['cart']),
        })
