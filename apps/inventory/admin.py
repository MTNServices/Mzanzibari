from django.contrib import admin
from .models import StockLevel, StockMovement


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity_on_hand', 'reorder_level', 'last_counted')
    list_filter = ('last_counted',)
    search_fields = ('product__name', 'product__sku')
    readonly_fields = ('product', 'last_counted')
    
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'movement_type', 'quantity', 'reason', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('stock__product__name', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    
    def product_name(self, obj):
        return obj.stock.product.name
    product_name.short_description = 'Product'
