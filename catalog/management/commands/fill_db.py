import json
from django.core.management.base import BaseCommand
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает БД и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        # Очищаем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Читаем фикстуру категорий
        with open("catalog/fixtures/category_data.json", "r", encoding="utf-8") as f:
            categories_data = json.load(f)

        categories_to_create = []
        for item in categories_data:
            categories_to_create.append(Category(id=item["pk"], **item["fields"]))
        Category.objects.bulk_create(categories_to_create)

        # Читаем фикстуру продуктов
        with open("catalog/fixtures/product_data.json", "r", encoding="utf-8") as f:
            products_data = json.load(f)

        products_to_create = []
        for item in products_data:
            # Для ForeignKey передаем ID категории напрямую через category_id
            fields = item["fields"]
            category_id = fields.pop("category")
            products_to_create.append(
                Product(id=item["pk"], category_id=category_id, **fields)
            )
        Product.objects.bulk_create(products_to_create)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval('catalog_category_id_seq', COALESCE((SELECT MAX(id) FROM catalog_category), 1));"
            )
            cursor.execute(
                "SELECT setval('catalog_product_id_seq', COALESCE((SELECT MAX(id) FROM catalog_product), 1));"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "База данных успешно перезаписана тестовыми данными. Счетчики синхронизированы"
            )
        )
