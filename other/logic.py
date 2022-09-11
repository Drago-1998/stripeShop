import os
from typing import Union

from item.models import Item
from other.models import Tax


def create_tax_in_stripe(tax_obj: Tax, old_stripe_id: Union[None, str] = None) -> str:
    """Create Tax in Stripe and return the id"""
    import stripe

    stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

    # If update tex deactivate old tax in Stripe
    if old_stripe_id:
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
