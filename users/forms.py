from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User

# Форма регистрации (Задание 2)
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Форма редактирования профиля (Дополнительное задание)
class UserProfileForm(UserChangeForm):
    # Удаляем поле пароля из этой формы для безопасности
    password = None

    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'