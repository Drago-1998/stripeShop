import os

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

    s_promo_code = stripe.Coupon.create(
        coupon=promo_code_obj.coupon.stripe_id,
        code=promo_code_obj.code,
        active=promo_code_obj.active,
    )

    return s_promo_code.id
