from django.urls import path
from blog.views import (
    BlogArticleListView,
    BlogArticleDetailView,
    BlogArticleCreateView,
    BlogArticleUpdateView,
    BlogArticleDeleteView,
)

# Устанавливаем пространство имен для приложения (чтобы не было конфликтов)
app_name = "blog"

urlpatterns = [
    # Маршруты для Блога
    path("blog/", BlogArticleListView.as_view(), name="blog_list"),
    path("blog/create/", BlogArticleCreateView.as_view(), name="blog_create"),
    path("blog/<int:pk>/", BlogArticleDetailView.as_view(), name="blog_detail"),
    path("blog/<int:pk>/update/", BlogArticleUpdateView.as_view(), name="blog_update"),
    path("blog/<int:pk>/delete/", BlogArticleDeleteView.as_view(), name="blog_delete"),
]
