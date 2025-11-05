from django.urls import path
from . import views

urlpatterns = [
    # Login & Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Export routes
    path('export_csv/', views.export_csv, name='export_csv'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),

    # AJAX Product Update
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
]
