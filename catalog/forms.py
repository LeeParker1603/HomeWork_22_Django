from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов (Задание 1)
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        # Указываем поля, которые пользователь заполняет в форме
        fields = ['name', 'price', 'category', 'photo', 'description', 'is_published']

        error_messages = {
            'photo': {
                'invalid_image': "Загруженный файл не является корректным изображением. Пожалуйста, выберите картинку.",
            }
        }

    def __init__(self, *args, **kwargs):
        """Стилизация формы под общую стилистику платформы """
        # Достаем пользователя (request.user) из переданных аргументов контроллера
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Задаем Bootstrap-класс для полей ввода (кроме чекбоксов)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Настройка плейсхолдеров
            if field_name == 'photo':
                field.widget.attrs['placeholder'] = "Допускаются форматы JPEG, PNG. Макс. размер: 5 МБ."
                field.help_text = "Доступные форматы: JPEG, PNG. Ограничение по размеру: не более 5 МБ."
            else:
                field.widget.attrs['placeholder'] = f"Введите {field.label.lower()}"

        # ДИНАМИЧЕСКАЯ ПРОВЕРКА ПРАВ:
        # Если пользователь НЕ суперпользователь и НЕ имеет права публикации — скрываем поле
        if not (self.user and (self.user.is_superuser or self.user.has_perm('catalog.can_unpublish_product'))):
            if 'is_published' in self.fields:
                del self.fields['is_published']

    def clean_name(self):
        """Валидация названия на запрещенные слова (Задание 1)"""
        name = self.cleaned_data.get('name')
        name_lower = name.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f"В названии товара нельзя использовать запрещенное слово: '{word}'.")
        return name

    def clean_description(self):
        """Валидация описания на запрещенные слова (Задание 1)"""
        description = self.cleaned_data.get('description', '')
        description_lower = description.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(f"В описании товара нельзя использовать запрещенное слово: '{word}'.")
        return description

    def clean_price(self):
        """Валидация цены: защита от отрицательных значений (Задание 2)"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной. Укажите корректную стоимость.")
        return price

    def clean_photo(self):
        """Дополнительное задание: Валидация формата и веса изображения (до 5 МБ)"""
        photo = self.cleaned_data.get('photo')

        if photo:
            # 1. Проверяем размер файла (5 МБ = 5 * 1024 * 1024 байт)
            max_size = 5 * 1024 * 1024
            if photo.size > max_size:
                raise ValidationError("Размер загружаемого файла не должен превышать 5 МБ.")

            # 2. Проверяем формат файла по его расширению
            filename = photo.name.lower()
            if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):
                raise ValidationError("Допускаются файлы только в формате JPEG или PNG.")

        return photo