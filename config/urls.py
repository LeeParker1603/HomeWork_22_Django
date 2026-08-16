from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Подключаем маршруты приложения catalog через include
    path('', include('catalog.urls')),
]