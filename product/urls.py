from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),

    #auth
    path('login/', auth_views.LoginView.as_view(template_name='product/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    #stats
    path('stats/', views.product_stats, name='product_stats'),

    #export
    path('export/', views.export_products_csv, name='export_products_csv'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)