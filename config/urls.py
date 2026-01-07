from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from apps.products.views import ProductViewSet
from apps.inventory.views import StockLevelViewSet, StockMovementViewSet
from apps.sales.views import SaleViewSet
from apps.purchases.views import PurchaseViewSet, SupplierViewSet

# DRF Router
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stock-levels', StockLevelViewSet, basename='stock-level')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'suppliers', SupplierViewSet, basename='supplier')

def api_root(request, **kwargs):
    context = {
        'message': 'mzanzibari POS API',
        'version': '1.1.0',
        'endpoints': [
            ('Products', '/api/products/'),
            ('Stock Levels', '/api/stock-levels/'),
            ('Stock Movements', '/api/stock-movements/'),
            ('Sales', '/api/sales/'),
            ('Purchases', '/api/purchases/'),
            ('Suppliers', '/api/suppliers/'),
            ('Admin', '/admin/'),
            ('API Schema', '/api/schema/'),
        ]
    }
    try:
        print(f"[api_root] request.path={request.path}")
    except Exception:
        pass
    return render(request, 'landing.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    # root -> api root for convenience
    path('', api_root, name='root'),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    # Catch-all: serve the landing page for any unmatched GET path (temporary fallback)
    path('<path:remaining>', api_root, name='catch-all'),
]
