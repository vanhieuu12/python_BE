from django.contrib import admin
from django.urls import path, include
from django.conf import settings  
from django.conf.urls.static import static
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls')),  
    path('stats/', views.product_stats, name='product_stats')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)