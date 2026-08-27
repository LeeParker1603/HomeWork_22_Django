from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ContactsTemplateView,
    ProductUpdateView,
    ProductDeleteView, ProductTogglePublishView
)

# Устанавливаем пространство имен для приложения (чтобы не было конфликтов)
app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"), # Создание
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'), # Редактирование
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'), # Удаление
    path('products/<int:pk>/toggle-publish/', ProductTogglePublishView.as_view(), name='product_toggle_publish'), # Модерация
]
