import decimal
import os
from typing import Union, Any

from django.db.models import Sum
from django.db.models.functions import Coalesce
from stripe.stripe_object import StripeObject

from item.models import Item, ItemToTax
from order.models import Order, OrderItem, DiscountToOrder


def create_stripe_checkout_session(items: list[dict], promos: list[dict]) -> Union[list, StripeObject]:
    """Create Stripe Checkout Session"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    item_objects = Item.objects.filter(id__in=(_item['id'] for _item in items)).in_bulk()
    tax_to_item_bundles = ItemToTax.objects \
        .select_related('tax', 'item') \
        .filter(item_id__in=(_item['id'] for _item in items)).in_bulk()
    item_data = {
        _item['id']: {
            'object': item_objects[_item['id']],
            'quantity': _item['quantity'],
            'taxes_stripe_ids': [
                tax_to_item_bundle.tax.stripe_id
                for tax_to_item_bundle in tax_to_item_bundles.values()
                if tax_to_item_bundle.item == item_objects[_item['id']]
            ]
        }
        for _item in items
    }
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": item_dict['object'].price_id,
                "quantity": item_dict['quantity'],
                "tax_rates": item_dict['taxes_stripe_ids']
            }
            for item_id, item_dict in item_data.items()
        ],
        success_url='http://localhost:8000/',
        cancel_url=f'http://localhost:8000/',
        mode='payment',
        discounts=[
            {
                'coupon': promo['coupon_stripe_id'],
                'promotion_code': promo['promo_stripe_id']
            }
            for promo in promos
        ]
    )
    return session


def pay_form_order(order_id):
    """
    This function get Order Id and create Stripe checkout Session
    and return this Session
    """
    order_items = OrderItem.objects \
        .select_related('item') \
        .filter(order_id=order_id) \
        .in_bulk()
    order_promos = DiscountToOrder.objects \
        .select_related('promo', 'coupon') \
        .filter(order_id=order_id) \
        .in_bulk()
    return create_stripe_checkout_session(
        [
            {
                'id': _order_item.item_id,
                'quantity': int(_order_item.quantity)
            }
            for _order_item in order_items.values()
        ],
        [
            {
                'coupon_stripe_id': order_promo.coupon.stripe_id,
                'promo_stripe_id': order_promo.promo.stripe_id
            }
            for order_promo in order_promos.values()
        ]
    )


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
    """Calculate Item price with Item Taxes"""
    percentage_total = item_obj.price * (decimal.Decimal(str(item_obj.taxes_percentage)) / decimal.Decimal('100'))
    return percentage_total + item_obj.price


def _calc_cart_item_total(item_obj: Item, quantity: Union[int, float]) -> decimal.Decimal:
    """Calculate Item total"""
    return decimal.Decimal(str(quantity)) * _calc_item_price_with_taxes(item_obj)


def filter_cart_with_currency(cart: list, currency: str) -> dict:
    """Filter Cart Items with picked currency"""
    return {
        cart_item_dict['id']: cart_item_dict
        for cart_item_dict in cart
        if cart_item_dict['currency'] == currency
    }


def create_order_from_cart(cart: dict, promos: dict) -> Order:
    """This function create order from cart
    and bind discount coupons and promotion codes"""
    order_total = sum(_cart_item['total'] for _cart_item in cart.values())
    promos_total_percent_off = sum(_promo['percent_off'] for _promo in promos.values())
    order_total_with_promos = order_total - (decimal.Decimal(str(promos_total_percent_off / 100)) * order_total)
    order = Order.objects.create(
        total=order_total,
        total_with_promos=order_total_with_promos
    )

    order_items = (
        OrderItem(
            order=order,
            item_id=_cart_item['id'],
            quantity=_cart_item['quantity'],
            total_with_taxes=_cart_item['price_with_taxes'],
        )
        for _cart_item in cart.values()
    )
    discount_ot_order_set = (
        DiscountToOrder(
            order=order,
            promo_id=_promo['id'],
            coupon_id=_promo['coupon_id']
        )
        for _promo in promos.values()
    )

    OrderItem.objects.bulk_create(order_items)
    DiscountToOrder.objects.bulk_create(discount_ot_order_set)

    return order
