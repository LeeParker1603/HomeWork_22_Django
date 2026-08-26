from django.contrib import admin
from blog.models import BlogArticle  # Импортируем из правильного места!


@admin.register(BlogArticle)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "views_count", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
