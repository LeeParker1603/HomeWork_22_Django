from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов и назначает права'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем тип контента для нашей модели продукта
        content_type = ContentType.objects.get_for_model(Product)

        # Ищем два нужных разрешения по их кодовым именам
        unpublish_perm = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        delete_perm = Permission.objects.get(codename='delete_product', content_type=content_type)

        # Назначаем права группе
        moderator_group.permissions.set([unpublish_perm, delete_perm])

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана и настроена!'))