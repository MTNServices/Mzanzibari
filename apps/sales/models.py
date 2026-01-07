from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.products.models import Product


User = get_user_model()


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('check', 'Check'),
        ('mpesa', 'M-Pesa'),
    ]

    sale_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sale {self.sale_number} - {self.total_amount}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.sale_number:
            from datetime import datetime
            import random
            self.sale_number = f"SALE-{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{random.randint(100, 999)}"
        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)

