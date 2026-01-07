from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_method', 'created_at']
    ordering_fields = ['total_amount', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        """Get sales for a specific date: /api/sales/daily_sales/?date=2024-01-15"""
        from datetime import datetime
        date_str = request.query_params.get('date', datetime.now().strftime('%Y-%m-%d'))
        sales = self.queryset.filter(created_at__date=date_str)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def total_by_method(self, request):
        """Get sales totals by payment method"""
        from django.db.models import Sum
        totals = self.queryset.values('payment_method').annotate(total=Sum('total_amount'))
        return Response(totals)

