from django.shortcuts import render

# product views placeholder
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer


class ProductListView(APIView):
	"""Allow anonymous GET; require authentication for POST."""

	def get_permissions(self):
		if self.request.method == 'GET':
			return [AllowAny()]
		return [IsAuthenticated()]

	def get(self, request):
		qs = Product.objects.all()
		serializer = ProductSerializer(qs, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
