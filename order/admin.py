from django.contrib import admin

from order.models import Order, OrderItem, DiscountToOrder


class OrderItemInline(admin.TabularInline):
    """Tabular Inline for Order Item"""
    model = OrderItem
    extra = 0
    fields = 'item', 'quantity', 'total_with_taxes'


class DiscountToOrderInline(admin.TabularInline):
    """Tabular Inline for Promotion codes and Coupons"""
    model = DiscountToOrder
    extra = 0
    fields = 'promo', 'coupon'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'total', 'total_with_promos'

    inlines = [
        OrderItemInline,
        DiscountToOrderInline
    ]
