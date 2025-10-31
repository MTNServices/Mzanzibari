from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'last_updated')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'stock')
        }),
    )

    readonly_fields = ('last_updated',)
