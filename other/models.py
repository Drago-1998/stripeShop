from django.db import models

from other.constants import TAX_TYPE_CHOICES, DURATION_CHOICES
from other.validators import percent_validator
from payment.constants import CURRENCY_CHOICES


class DiscountCoupon(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description', default='')
    percent_off = models.FloatField(verbose_name='Percent off', validators=[percent_validator])
    duration = models.CharField(verbose_name='Duration',
                                max_length=255,
                                default='once',
                                choices=DURATION_CHOICES)
    stripe_id = models.CharField(verbose_name='Stripe ID', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        from other.logic import create_coupon_in_stripe

        self.price_id = create_coupon_in_stripe(self)
        super(DiscountCoupon, self).save(**kwargs)

    class Meta:
        verbose_name_plural = 'Discount Coupons'
        verbose_name = 'Discount Coupon'


class PromoCode(models.Model):
    code = models.CharField(verbose_name='Code', max_length=255)
    coupon = models.ForeignKey('DiscountCoupon', verbose_name='Купон', on_delete=models.PROTECT)
    active = models.BooleanField(verbose_name='Active', default=True)
    stripe_id = models.CharField(verbose_name='Stripe ID', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.code

    def save(self, **kwargs):
        from other.logic import create_promo_code_in_stripe

        self.price_id = create_promo_code_in_stripe(self)
        super(PromoCode, self).save(**kwargs)

    class Meta:
        verbose_name_plural = 'Promo Codes'
        verbose_name = 'Promo Code'


class Tax(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description', default='')
    percentage = models.FloatField(verbose_name='Percentage', validators=[percent_validator])
    stripe_id = models.CharField(verbose_name='Stripe ID', max_length=255, null=True, blank=True)
    tax_type = models.CharField(verbose_name='Tax type',
                                max_length=9,
                                default='vat',
                                choices=TAX_TYPE_CHOICES)
    active = models.BooleanField(verbose_name='Active', default=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        from other.logic import create_tax_in_stripe

        self.price_id = create_tax_in_stripe(self)
        super(Tax, self).save(**kwargs)

    class Meta:
        verbose_name_plural = 'Taxes'
        verbose_name = 'Tax'
