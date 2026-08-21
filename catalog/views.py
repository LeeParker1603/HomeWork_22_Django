from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from catalog.models import Product, Category, ContactInfo


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products_list"
    paginate_by = 6  # Пагинация сохраняется встроенными средствами ListView
    queryset = Product.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories_list"] = Category.objects.all()
        # Доп. задание: вывод последних 5 продуктов в консоль при каждом запросе
        latest_products = Product.objects.all().order_by("-created_at")[:5]
        print("--- Последние 5 продуктов ---")
        for product in latest_products:
            print(f"Товар: {product.name} | Цена: {product.price}")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        # Метод автоматически увеличивает количество просмотров при открытии товара
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class ProductCreateView(CreateView):
    model = Product
    template_name = "catalog/product_form.html"
    fields = ["name", "price", "category", "photo", "description"]
    success_url = reverse_lazy("catalog:home")

    # Переопределяем метод, чтобы вывести переменную 'categories' в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем список всех категорий для вашего цикла {% for %}
        context["categories"] = Category.objects.all()
        return context


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_data"] = ContactInfo.objects.first()
        return context


# def home_view(request):
#     # Лаконичный запрос ко всем продуктам
#     products_all = Product.objects.all().order_by('-created_at')
#
#     # Реализация пагинации: выводим по 6 товаров на страницу
#     paginator = Paginator(products_all, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # Доп. задание из прошлой работы: вывод последних 5 в консоль
#     latest_products = Product.objects.all().order_by('-created_at')[:5]
#     print("--- Последние 5 продуктов ---")
#     for product in latest_products:
#         print(f"Товар: {product.name} | Цена: {product.price}")
#
#     context = {
#         'page_obj': page_obj  # Передаем объект пагинации вместо простого списка
#     }
#     return render(request, 'catalog/home.html', context)
#
#
# def product_detail_view(request, pk):
#     # Извлечение одного объекта через ORM по pk с защитой от ошибок (404)
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'product': product
#     }
#     return render(request, 'catalog/product_detail.html', context)
#
#
# def product_create_view(request):
#     # Дополнительное задание: Страница формы создания товара
#     categories = Category.objects.all()
#     errors = {}
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         category_id = request.POST.get('category')
#         description = request.POST.get('description', '')
#         photo = request.FILES.get('photo')  # Получаем загруженный файл изображения
#
#         # Базовая валидация (поля обязательны)
#         if not name:
#             errors['name'] = 'Укажите наименование товара.'
#         if not price:
#             errors['price'] = 'Укажите цену товара.'
#         if not category_id:
#             errors['category'] = 'Выберите категорию.'
#
#         if not errors:
#             # Сохранение нового товара в БД
#             category = get_object_or_404(Category, pk=category_id)
#             new_product = Product.objects.create(
#                 name=name,
#                 price=price,
#                 category=category,
#                 description=description,
#                 photo=photo
#             )
#             return redirect('catalog:product_detail', pk=new_product.pk)
#
#     context = {
#         'categories': categories,
#         'errors': errors
#     }
#     return render(request, 'catalog/product_form.html', context)
#
#
#
# def contacts_view(request):
#     if request.method == 'POST':
#         # Здесь остается ваша старая логика обработки формы (если она была),
#         # например, получение name, phone, message из request.POST
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f"Новое сообщение от {name} ({phone}): {message}")
#
#     # Извлекаем из базы данных САМУЮ ПЕРВУЮ запись с контактами
#     contact_data = ContactInfo.objects.first()
#
#     # Передаем объект с контактами в словарь контекста шаблона
#     context = {
#         'contact_data': contact_data
#     }
#
#     return render(request, 'catalog/contacts.html', context)
