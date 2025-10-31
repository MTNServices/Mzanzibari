from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'), name='index'),
    path('product/', include('apps.product.urls')),
    path('test_marquee/', TemplateView.as_view(template_name='test_marquee.html'), name='test_marquee'),
]
