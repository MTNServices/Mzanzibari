from django.contrib import admin
from django.urls import path, include
from app import views as app_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('', app_views.login_view, name='login'),
    path('logout/', app_views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', app_views.dashboard, name='dashboard'),

    # Export routes
    path('export/csv/', app_views.export_csv, name='export_csv'),
    path('export/excel/', app_views.export_excel, name='export_excel'),
    path('export/pdf/', app_views.export_pdf, name='export_pdf'),

    # ✅ Include product app URLs
    path('product/', include('product.urls')),
]
