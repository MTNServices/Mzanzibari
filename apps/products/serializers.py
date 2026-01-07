from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'sku', 'price', 'created_at', 'updated_at']

	def validate_price(self, value):
		if value < 0:
			raise serializers.ValidationError('Price must be non-negative.')
		return value
