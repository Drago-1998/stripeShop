import os

from item.models import Item


def create_product_in_stripe(item_obj: Item) -> tuple[str, str]:
    """Create Product and Price in Stripe and return their ids"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    s_product = stripe.Product.create(
        name=item_obj.name,
        description=item_obj.description
    )
    s_price = stripe.Price.create(
        unit_amount_decimal=item_obj.price * 100,
        currency=item_obj.currency,
        product=s_product.id,
    )

    return s_product.id, s_price.id


def update_product_in_stripe(item_obj: Item) -> str:
    """Update Product and Create Price in Stripe and return price id"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    stripe.Product.modify(
        item_obj.stripe_id,
        name=item_obj.name,
        description=item_obj.description
    )
    s_price = stripe.Price.create(
        unit_amount_decimal=item_obj.price * 100,
        currency=item_obj.currency,
        product=item_obj.stripe_id,
    )

    return s_price.id