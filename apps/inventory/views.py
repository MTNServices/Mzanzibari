from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import StockLevel, StockMovement
from .serializers import StockLevelSerializer, StockMovementSerializer


class StockLevelViewSet(viewsets.ModelViewSet):
    queryset = StockLevel.objects.all()
    serializer_class = StockLevelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['quantity_on_hand']
    ordering_fields = ['quantity_on_hand', 'reorder_level']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['movement_type', 'stock']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [AllowAny]

