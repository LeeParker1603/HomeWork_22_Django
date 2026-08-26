from django.db import models
from django.utils.text import slugify


class BlogArticle(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=200, verbose_name="slug", blank=True, null=True)
    content = models.TextField(verbose_name="Содержимое")
    photo = models.ImageField(
        upload_to="blog/", verbose_name="Превью (изображение)", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Автоматическая генерация slug из заголовка при сохранении
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

    def __str__(self):
        return self.title
