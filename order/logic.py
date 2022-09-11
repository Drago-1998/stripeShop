import decimal
import os
from typing import Union, Any

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from stripe.stripe_object import StripeObject

from item.models import Item


def create_stripe_checkout_session(items_ids: list) -> Union[list, StripeObject]:
    """Create Stripe Checkout Session"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    items = Item.objects.filter(id__in=items_ids)
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": item.price_id,
                "quantity": 1,
            }
            for item in items
        ],
        success_url='http://localhost:8000/',
        cancel_url=f'http://localhost:8000/',
        mode='payment'
    )
    return session


def add_item_in_cart(cart: Union[dict, bool], item_id: int) -> dict:
    """Add Item in Cart"""
    _item_id = str(item_id)
    if not cart:
        cart = {}

    if _item_id in cart:
        cart[_item_id] += 1
    else:
        cart[_item_id] = 1

    return cart


def sub_item_in_cart(cart: dict, item_id: int) -> dict:
    """Remove Item from Cart"""
    _item_id = str(item_id)
    try:
        cart[_item_id] -= 1
        if cart[_item_id] == 0:
            del cart[_item_id]

        return cart
    except KeyError:
        raise KeyError('Item(id=%d) not found in Cart' % item_id)


def cart_items_info(cart: dict) -> list[dict[str, Any]]:
    """Get Item from database for cart"""
    items = Item.objects.filter(id__in=(
        _item_id for _item_id in cart.keys()
    )).annotate(
        taxes_percentage=Coalesce(Sum('taxes_bundles__tax__percentage'), 0.0)
    ).in_bulk()
    return [
        {
            'id': _item_id,
            'name': _item_obj.name,
            'description': _item_obj.description,
            'price': _item_obj.price,
            'currency': _item_obj.currency,
            'taxes_percentage': _item_obj.taxes_percentage,
            'price_with_taxes': _calc_item_price_with_taxes(_item_obj),
            'quantity': cart[str(_item_id)],
            'total': _calc_cart_item_total(_item_obj, cart[str(_item_id)]),
        }
        for _item_id, _item_obj in items.items()
    ]


def _calc_item_price_with_taxes(item_obj: Item) -> decimal.Decimal:
    percentage_total = item_obj.price * (decimal.Decimal(str(item_obj.taxes_percentage)) / decimal.Decimal('100'))
    return percentage_total + item_obj.price


def _calc_cart_item_total(item_obj: Item, quantity: Union[int, float]) -> decimal.Decimal:
    return decimal.Decimal(str(quantity)) * _calc_item_price_with_taxes(item_obj)
