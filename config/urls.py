from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
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

def api_root(request):
    return JsonResponse({
        'message': 'mzanzibari POS API v1.1',
        'version': '1.1.0',
        'endpoints': {
            'products': '/api/products/',
            'stock_levels': '/api/stock-levels/',
            'stock_movements': '/api/stock-movements/',
            'sales': '/api/sales/',
            'purchases': '/api/purchases/',
            'suppliers': '/api/suppliers/',
            'admin': '/admin/',
            'docs': '/api/schema/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    # root -> api root for convenience
    path('', api_root, name='root'),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
