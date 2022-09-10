import os

from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'US dollars'),
        ('rub', 'Russian rubles')
    )

    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(verbose_name='Price', max_digits=15, decimal_places=2)
    currency = models.CharField(verbose_name='Currency', max_length=8, default='usd', choices=CURRENCY_CHOICES)
    stripe_id = models.CharField(verbose_name='StripeId', max_length=255, blank=True, null=True)
    price_id = models.CharField(verbose_name='StripeId', max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.price} $'

    def save(self, **kwargs):
        import stripe

        stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

        if not self.id:
            s_product = stripe.Product.create(
                name=self.name,
                description=self.description
            )
            s_price = stripe.Price.create(
                unit_amount_decimal=self.price * 100,
                currency=self.currency,
                product=s_product.id,
            )
            self.stripe_id = s_product.id
            self.price_id = s_price.id
        else:
            stripe.Product.modify(
                self.stripe_id,
                name=self.name,
                description=self.description
            )
            s_price = stripe.Price.create(
                unit_amount_decimal=self.price * 100,
                currency=self.currency,
                product=self.stripe_id,
            )
            self.price_id = s_price.id
        super(Item, self).save(**kwargs)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class ItemToTax(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey('Item', verbose_name='Item (Product)', on_delete=models.CASCADE)
    tax = models.ForeignKey('other.Tax', verbose_name='Tax', on_delete=models.PROTECT)
