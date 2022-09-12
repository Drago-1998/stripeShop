from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(verbose_name='Order total', max_digits=15, decimal_places=2)
    total_with_promos = models.DecimalField(verbose_name='Order total with discount', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'


class OrderItem(models.Model):
    order = models.ForeignKey('Order',
                              verbose_name='Order',
                              related_name='order_items',
                              on_delete=models.CASCADE)
    item = models.ForeignKey('item.Item', verbose_name='Item (Product)', on_delete=models.PROTECT)
    quantity = models.DecimalField(verbose_name='Quantity', max_digits=11, decimal_places=2)
    total_with_taxes = models.DecimalField(verbose_name='Total with Taxes', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Order elements'
        verbose_name = 'Order element'


class DiscountToOrder(models.Model):
    """For bond Order with Promo Codes and Discount Coupons"""
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order',
                              verbose_name='Order',
                              related_name='discount_bundles',
                              on_delete=models.PROTECT)
    promo = models.ForeignKey('other.PromoCode',
                              verbose_name='Promo',
                              related_name='order_bundles',
                              on_delete=models.PROTECT,
                              blank=True, null=True)
    coupon = models.ForeignKey('other.DiscountCoupon',
                               verbose_name='Coupon',
                               related_name='order_bundles',
                               on_delete=models.PROTECT)
