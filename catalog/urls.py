from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ContactsTemplateView
from catalog.views import (
    BlogArticleListView, BlogArticleDetailView,
    BlogArticleCreateView, BlogArticleUpdateView, BlogArticleDeleteView
)

# Устанавливаем пространство имен для приложения (чтобы не было конфликтов)
app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),

# Маршруты для Блога
    path('blog/', BlogArticleListView.as_view(), name='blog_list'),
    path('blog/create/', BlogArticleCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/', BlogArticleDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/update/', BlogArticleUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', BlogArticleDeleteView.as_view(), name='blog_delete'),
]