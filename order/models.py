from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', verbose_name='Order', on_delete=models.CASCADE)
    item = models.ForeignKey('item.Item', verbose_name='Item (Product)', on_delete=models.PROTECT)
    quantity = models.DecimalField(verbose_name='Quantity', max_digits=11, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Order elements'
        verbose_name = 'Order element'
