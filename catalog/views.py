from django.shortcuts import render
from catalog.models import Product, ContactInfo


def home_view(request):
    # 1. Берем ВСЕ продукты из базы данных для отображения на сайте
    products_list = Product.objects.all()

    # 2. Дополнительное задание: берем последние 5 созданных для вывода в консоль
    latest_products = Product.objects.all().order_by('-created_at')[:5]

    print("--- Последние 5 продуктов ---")
    for product in latest_products:
        print(f"Товар: {product.name} | Цена: {product.price}")
    print("-----------------------------")

    # 3. Формируем контекст, где ключ 'products_list' строго совпадает с циклом в HTML
    context = {
        'products_list': products_list
    }

    # 4. ОБЯЗАТЕЛЬНО передаем context третьим аргументом!
    return render(request, 'catalog/home.html', context)



def contacts_view(request):
    if request.method == 'POST':
        # Здесь остается ваша старая логика обработки формы (если она была),
        # например, получение name, phone, message из request.POST
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({phone}): {message}")

    # Извлекаем из базы данных САМУЮ ПЕРВУЮ запись с контактами
    contact_data = ContactInfo.objects.first()

    # Передаем объект с контактами в словарь контекста шаблона
    context = {
        'contact_data': contact_data
    }

    return render(request, 'catalog/contacts.html', context)