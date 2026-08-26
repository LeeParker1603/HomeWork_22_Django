from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from blog.models import BlogArticle
from django.contrib.auth.mixins import PermissionRequiredMixin


# 1. Список опубликованных статей
class BlogArticleListView(ListView):
    model = BlogArticle
    template_name = "blog/blog_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        """Контент-менеджер видит все статьи (включая черновики), гости — только опубликованные"""
        user = self.request.user

        # Если пользователь авторизован и имеет право редактировать статьи (Контент-менеджер) или админ
        if user.is_authenticated and (user.has_perm('blog.change_blogarticle') or user.is_superuser):
            return BlogArticle.objects.all().order_by('-created_at')

        # Все остальные (обычные пользователи и анонимные гости) видят только опубликованный контент
        return BlogArticle.objects.filter(is_published=True).order_by('-created_at')


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
class BlogArticleCreateView(PermissionRequiredMixin, CreateView):
    model = BlogArticle
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "photo", "is_published"]
    permission_required = 'blog.add_blogarticle'  # Проверка права

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


# 4. Редактирование статьи
class BlogArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = BlogArticle
    template_name = "blog/blog_form.html"
    fields = ["title", "content", "photo", "is_published"]
    permission_required = 'blog.change_blogarticle'  # Проверка права

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


# 5. Удаление статьи
class BlogArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = BlogArticle
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
    permission_required = 'blog.delete_blogarticle'  # Проверка права
