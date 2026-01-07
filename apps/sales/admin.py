from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_number', 'user_name', 'total_amount', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('sale_number', 'user__username', 'notes')
    readonly_fields = ('sale_number', 'total_amount', 'created_at', 'updated_at')
    inlines = [SaleItemInline]
    
    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username if obj.user else 'Unknown'
    user_name.short_description = 'Cashier'


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale_number', 'product_name', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('sale__created_at',)
    search_fields = ('sale__sale_number', 'product__name')
    readonly_fields = ('subtotal',)
    
    def sale_number(self, obj):
        return obj.sale.sale_number
    sale_number.short_description = 'Sale'
    
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'
