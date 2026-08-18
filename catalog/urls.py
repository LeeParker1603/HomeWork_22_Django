from django.urls import path
from .views import home_view, contacts_view

# Устанавливаем пространство имен для приложения (чтобы не было конфликтов)
app_name = 'catalog'

urlpatterns = [
    # Главная страница (пустой путь, но по критериям для Django корень оставляют так)
    path('', home_view, name='home'),

    # Страница контактов (обязательно со слэшем на конце по ТЗ)
    path('contacts/', contacts_view, name='contacts'),
]