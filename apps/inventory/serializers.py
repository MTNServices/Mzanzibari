from rest_framework import serializers
from .models import StockLevel, StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='stock.product.name', read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'stock', 'product_name', 'movement_type', 'quantity', 'reason', 'created_at']


class StockLevelSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    movements = StockMovementSerializer(many=True, read_only=True)

    class Meta:
        model = StockLevel
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity_on_hand', 'reorder_level', 'needs_reorder', 'last_counted', 'movements']

