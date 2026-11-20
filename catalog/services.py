from django.core.cache import cache
from django.conf import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция, возвращающая список опубликованных продуктов
    в указанной категории с использованием низкоуровневого кеширования.
    """
    # Если кеширование глобально отключено в настройках, берем данные напрямую
    if not settings.CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)

    # Ключ для хранения в Redis
    key = f'products_category_{category_id}'

    # Пытаемся достать данные из кэша Redis
    products = cache.get(key)

    # Если в кэше пусто — делаем запрос в PostgreSQL и сохраняем в кэш
    if products is None:
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(key, products, timeout=60 * 15)  # Кэшируем на 15 минут

    return products