from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from blog.models import BlogArticle


# 1. Список опубликованных статей
class BlogArticleListView(ListView):
    model = BlogArticle
    template_name = "blog/blog_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


# 2. Детальный просмотр статьи (+1 к просмотрам)
class BlogArticleDetailView(DetailView):
    model = BlogArticle
    template_name = "blog/blog_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


# 3. Создание статьи
class BlogArticleCreateView(CreateView):
    model = BlogArticle
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "photo", "is_published"]

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


# 4. Редактирование статьи
class BlogArticleUpdateView(UpdateView):
    model = BlogArticle
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "photo", "is_published"]

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


# 5. Удаление статьи
class BlogArticleDeleteView(DeleteView):
    model = BlogArticle
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
