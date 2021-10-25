from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from qfit import views

from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('admin-panel/', include('adminpanel.urls')),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

