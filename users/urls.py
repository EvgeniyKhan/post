from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import ProfileView, SubscriptionCreate, UserRegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("perform_create/", SubscriptionCreate.as_view(), name="perform_create"),
]

"""
URL-шаблоны для аутентификации пользователя и управления профилем.

- 'login': Отображает страницу входа с использованием LoginView Django и пользовательским шаблоном.
- 'logout': Выходит из системы пользователя с использованием LogoutView Django.
- 'register': Отображает страницу регистрации с использованием UserRegisterView.
- 'profile': Отображает страницу профиля пользователя с использованием ProfileView.
- 'perform_create': Эндпоинт для выполнения операции создания, вероятно, создание объекта.
"""
