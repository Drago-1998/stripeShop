from django.contrib import admin

from item.models import Item, ItemToTax


class ItemToTaxInline(admin.TabularInline):
    model = ItemToTax
    extra = 0
    fields = ('tax',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = 'name', 'description', 'price', 'currency'

    inlines = [
        ItemToTaxInline
    ]
