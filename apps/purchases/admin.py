from django.contrib import admin
from .models import Supplier, Purchase, PurchaseItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    fields = ('name', 'email', 'phone', 'address', 'created_at')


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_number', 'supplier_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('purchase_number', 'supplier__name', 'notes')
    readonly_fields = ('purchase_number', 'total_amount', 'created_at', 'updated_at')
    inlines = [PurchaseItemInline]
    fieldsets = (
        ('Purchase Info', {
            'fields': ('purchase_number', 'supplier', 'status', 'user')
        }),
        ('Totals', {
            'fields': ('total_amount',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def supplier_name(self, obj):
        return obj.supplier.name if obj.supplier else 'Unknown'
    supplier_name.short_description = 'Supplier'


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_number', 'product_name', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('purchase__created_at',)
    search_fields = ('purchase__purchase_number', 'product__name')
    readonly_fields = ('subtotal',)
    
    def purchase_number(self, obj):
        return obj.purchase.purchase_number
    purchase_number.short_description = 'Purchase'
    
    def product_name(self, obj):
        return obj.product.name if obj.product else 'Unknown'
    product_name.short_description = 'Product'
