from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm


# Контроллер регистрации с отправкой приветственного письма
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # 1. Сохраняем пользователя в базу данных
        user = form.save()

        # 2. Отправка приветственного письма по заданию
        try:
            send_mail(
                subject='Добро пожаловать в Skystore!',
                message=f'Здравствуйте!\n\nСпасибо за регистрацию на нашей платформе Skystore.\nВаш логин для входа: {user.email}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")

        return super().form_valid(form)


# Авторизация по email (Задание 2)
class UserLoginView(LoginView):
    template_name = 'users/login.html'


# Выход из системы
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


# Редактирование профиля (Дополнительное задание)
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        # Возвращает текущего авторизованного пользователя
        return self.request.user
