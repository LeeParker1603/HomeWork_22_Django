from django.urls import path
from .views import home_view, contacts_view, product_detail_view, product_create_view

# Устанавливаем пространство имен для приложения (чтобы не было конфликтов)
app_name = 'catalog'

urlpatterns = [
    path('', home_view, name='home'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('products/create/', product_create_view, name='product_create'),

    # Страница контактов (обязательно со слэшем на конце по ТЗ)
    path('contacts/', contacts_view, name='contacts'),
]