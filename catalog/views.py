from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from catalog.models import Product, Category, ContactInfo
from catalog.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin


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

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm  # Используем форму и для редактирования
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        # После редактирования возвращаем пользователя на детальную страницу товара
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


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