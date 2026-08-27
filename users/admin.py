from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'country', 'is_staff', 'is_active')
    search_fields = ('email', 'phone')

    # Переводит вертикальный список групп в удобные две колонки
    filter_horizontal = ('groups', 'user_permissions')

    # Настройки отображения полей внутри карточки пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'phone', 'country', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Добавляем сортировку по id или email
    ordering = ('id',)