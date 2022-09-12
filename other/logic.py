import os
from typing import Union

from django.http import JsonResponse

from other.models import Tax, DiscountCoupon, PromoCode


def create_tax_in_stripe(tax_obj: Tax) -> str:
    """Create Tax in Stripe and return the id"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    # If update tex deactivate old tax in Stripe
    if tax_obj.stripe_id:
        stripe.TaxRate.modify(
            tax_obj.stripe_id,
            active=False,
        )

    s_tax = stripe.TaxRate.create(
        display_name=tax_obj.name,
        description=tax_obj.description,
        percentage=tax_obj.percentage,
        tax_type=tax_obj.tax_type,
        active=tax_obj.active,
        inclusive=False,
    )

    return s_tax.id


def create_coupon_in_stripe(coupon_obj: DiscountCoupon) -> str:
    """Create Coupon in Stripe and return the id"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    # If update tex delete old coupon in Stripe
    if coupon_obj.stripe_id:
        stripe.Coupon.delete(coupon_obj.stripe_id)

    s_coupon = stripe.Coupon.create(
        percent_off=coupon_obj.percent_off,
        duration=coupon_obj.duration,
        name=coupon_obj.name,
    )

    return s_coupon.id


def create_promo_code_in_stripe(promo_code_obj: PromoCode) -> str:
    """Create Promo Code in Stripe and return the id"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    # If update tex deactivate old promo_code in Stripe
    if promo_code_obj.stripe_id:
        stripe.PromotionCode.modify(
            promo_code_obj.stripe_id,
            active=False,
        )

    s_promo_code = stripe.PromotionCode.create(
        coupon=promo_code_obj.coupon.stripe_id,
        code=promo_code_obj.code,
        active=promo_code_obj.active,
    )

    return s_promo_code.id


def add_promo_code(promos: Union[dict, bool], promo_code: str) -> Union[dict, JsonResponse]:
    """Add Promo Code in Cart or return error response"""
    if not promos:
        promos = {}

    if promo_code in promos:
        return JsonResponse({
            'status': 'Error',
            'message': 'This promo code is already in your cart'
        })
    try:
        promo = PromoCode.objects.select_related('coupon')\
            .get(code=promo_code, active=True)
        promos[promo_code] = {
            'id': promo.id,
            'coupon_id': promo.coupon_id,
            'code': promo.code,
            'percent_off': promo.coupon.percent_off,
            'name': promo.coupon.name,
        }
    except PromoCode.DoesNotExist:
        return JsonResponse({
            'status': 'Error',
            'message': 'This promo code was not found or is no longer active'
        })

    return promos


def delete_promo_code(promos: dict, promo_code: str) -> dict:
    """Delete Promo Code from Cart or return error response"""
    del promos[promo_code]
    return promos
