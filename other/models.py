from django.db import models

from other.validators import percent_validator


class Discount(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description', default='')
    percent_off = models.FloatField(verbose_name='Percent off', validators=[percent_validator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Discounts'
        verbose_name = 'Discount'


class Tax(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description', default='')
    percentage = models.FloatField(verbose_name='Percent off', validators=[percent_validator])
    stripe_id = models.CharField(verbose_name='Stripe ID', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Taxes'
        verbose_name = 'Tax'
