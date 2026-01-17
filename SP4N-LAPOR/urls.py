from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.beranda, name='beranda'),
    path('masuk/', views.masuk, name='masuk'),
    path('daftar/', views.daftar, name='register'),
    path('logout/', views.keluar, name='keluar'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan_saya/', views.laporan_saya, name='laporan_saya'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-status/<int:laporan_id>/', views.update_status, name='update_status'),
    path('laporan/detail/<int:laporan_id>/', views.detail_laporan, name='detail_laporan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
