from rest_framework import serializers
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']


class SaleSerializer(serializers.ModelSerializer):
    sale_number = serializers.CharField(read_only=True)
    items = SaleItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'sale_number', 'user', 'username', 'total_amount', 'payment_method', 'notes', 'items', 'created_at', 'updated_at']

