from rest_framework import serializers
from .models import Purchase, PurchaseItem, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at']


class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_number = serializers.CharField(read_only=True)
    items = PurchaseItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'purchase_number', 'supplier', 'supplier_name', 'user', 'username', 'total_amount', 'status', 'notes', 'items', 'created_at', 'updated_at']

