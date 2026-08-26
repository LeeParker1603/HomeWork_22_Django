from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, UserLogoutView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]