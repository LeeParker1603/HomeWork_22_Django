from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from catalog.models import Product, Category, ContactInfo
from catalog.forms import ProductForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from catalog.services import get_products_by_category
from django.core.cache import cache


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products_list"
    paginate_by = 6  # Пагинация сохраняется встроенными средствами ListView

    def get_queryset(self):
        """Динамическая фильтрация товаров в зависимости от прав пользователя"""
        user = self.request.user

        # Кешируем выборку только для неавторизованных гостей (так как у них список статичен)
        if not user.is_authenticated:
            key = 'public_products_list'
            products = cache.get(key)

            if products is None:
                # Если в Redis пусто — делаем тяжелый SQL-запрос
                products = list(Product.objects.filter(is_published=True).order_by('-created_at'))
                # Сохраняем результат в кэш на 10 минут
                cache.set(key, products, timeout=60 * 10)
            return products

        # Если пользователь — суперпользователь или модератор с правом публикации
        if user.is_authenticated and (user.is_superuser or user.has_perm('catalog.can_unpublish_product')):
            return Product.objects.all().order_by('-created_at')

        # If пользователь авторизован, он видит опубликованные ПЛЮС свои собственные на модерации
        if user.is_authenticated:
            from django.db.models import Q
            return Product.objects.filter(Q(is_published=True) | Q(owner=user)).order_by('-created_at')

        # Анонимные гости видят ТОЛЬКО опубликованные товары
        return Product.objects.filter(is_published=True).order_by('-created_at')

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


class CategoryProductsListView(ListView):
    """Представление для отображения продуктов по конкретной категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Используем сервисную функцию
        return get_products_by_category(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем саму категорию в контекст для заголовка
        from django.shortcuts import get_object_or_404
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    # Переопределяем метод, чтобы вывести переменную 'categories' в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем список всех категорий для цикла {% for %}
        context["categories"] = Category.objects.all()
        return context

        # Пункт 2: Автоматически привязываем продукт к авторизованному пользователю

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user  # Записываем текущего пользователя в владельцы
        product.save()
        return super().form_valid(form)

    # Передаем request.user в форму
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm  # Используем форму и для редактирования
    template_name = 'catalog/product_form.html'

    # Проверка прав: пользователь должен иметь либо глобальное право изменения, либо кастомное право модератора
    permission_required = 'catalog.change_product'

    def has_permission(self):
        # Переопределяем метод, чтобы модератор с кастомным правом тоже мог зайти в форму редактирования
        perms = [self.permission_required, 'catalog.can_unpublish_product']
        return any(self.request.user.has_perm(perm) for perm in perms)

    # [ДОБАВИТЬ ЭТОТ МЕТОД] Сброс кэша при сохранении изменений автором
    def form_valid(self, form):
        response = super().form_valid(form)

        # Очищаем кэш, так как данные продукта обновились
        cache.delete('public_products_list')
        cache.delete(f'products_category_{self.object.category_id}')
        cache.clear()

        return response

    def get_success_url(self):
        # После редактирования возвращаем пользователя на детальную страницу товара
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # Проверяем, является ли текущий пользователь владельцем или суперпользователем
        return user == product.owner or user.has_perm('catalog.can_unpublish_product') or user.is_superuser

    # Передаем request.user в форму
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        # Условие: текущий пользователь — владелец, ИЛИ суперпользователь,
        # ИЛИ модератор со специальным системным правом удаления продуктов
        is_owner = user == product.owner
        is_moderator = user.has_perm('catalog.delete_product')

        return is_owner or is_moderator or user.is_superuser


class ProductTogglePublishView(PermissionRequiredMixin, View):
    """Контроллер для быстрой публикации/снятия с публикации товара модератором"""
    # Защищаем контроллер кастомным правом доступа из Задания 1
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Меняем статус публикации
        product.is_published = not product.is_published
        product.save()

        # ИНВАЛИДАЦИЯ КЭША (Сброс):
        cache.clear()

        # ПЕРЕХОД: Перенаправляем модератора строго на главную страницу каталога
        return redirect('catalog:home')


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_data"] = ContactInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Печатаем данные в консоль PyCharm (как требовалось в прошлых ДЗ)
        print(f"\n--- Новое сообщение из формы контактов ---")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print(f"-----------------------------------------\n")

        # Получаем контекст, чтобы страница не вернула ошибку при перезагрузке
        context = self.get_context_data()
        # Добавляем сообщение об успешной отправке для пользователя
        context['success'] = True

        return render(request, self.template_name, context)