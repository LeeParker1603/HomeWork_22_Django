from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogArticle

class Command(BaseCommand):
    help = 'Создает группу Контент-менеджер блога и назначает полные права на CRUD статей'

    def handle(self, *args, **options):
        # 1. Создаем или получаем группу контент-менеджеров
        group, created = Group.objects.get_or_create(name='Контент-менеджер блога')

        # 2. Получаем тип контента для нашей блоговой модели
        content_type = ContentType.objects.get_for_model(BlogArticle)

        # 3. Извлекаем из базы данных все системные права для этой модели (add, change, delete, view)
        permissions = Permission.objects.filter(content_type=content_type)

        # 4. Назначаем эти права группе
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер блога" успешно создана. Права на CRUD статей назначены!'))