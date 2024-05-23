from django.contrib import admin
from django.urls import path
from parser_app.views import CarViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cars/', CarViewSet.as_view({'get': 'list'}), name='car-list'),
    path('api/cars/upload_file/', CarViewSet.as_view({'post': 'create'}), name='upload-file'),
    path('api/cars/clear/', CarViewSet.as_view({'delete': 'destroy'}), name='clear-cars'),
    path('api/cars/<int:pk>/', CarViewSet.as_view({'get': 'retrieve'}), name='car-detail'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
