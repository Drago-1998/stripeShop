from django.contrib import admin

from other.models import Tax, PromoCode, DiscountCoupon


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = 'name', 'percentage', 'tax_type'
    list_filter = 'tax_type', 'percentage'


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = 'code', 'active'


@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    list_display = 'name', 'percent_off', 'duration'
    list_filter = 'percent_off', 'duration'
