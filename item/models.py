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
        from order.logic import create_product_in_stripe, update_product_in_stripe

        if not self.id:
            self.stripe_id, self.price_id = create_product_in_stripe(self)
        else:
            self.price_id = update_product_in_stripe(self)
        super(Item, self).save(**kwargs)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class ItemToTax(models.Model):
    """item to Tax bundle"""
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey('Item',
                             verbose_name='Item (Product)',
                             on_delete=models.CASCADE,
                             related_name='taxes_bundles')
    tax = models.ForeignKey('other.Tax',
                            verbose_name='Tax',
                            on_delete=models.PROTECT,
                            related_name='items_bundles')
