from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product with filtering, searching, and pagination."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['name', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'])
    def by_price_range(self, request):
        """Filter products by price range: /api/products/by_price_range/?min=10&max=100"""
        min_price = request.query_params.get('min', 0)
        max_price = request.query_params.get('max', 999999)
        products = self.queryset.filter(price__gte=min_price, price__lte=max_price)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# Keep old class-based view for backward compatibility
class ProductListView(APIView):
    """Deprecated: Use ProductViewSet instead."""
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

