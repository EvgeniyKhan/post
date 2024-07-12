from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserProfileForm, UserRegisterForm
from users.models import Subscription, User
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class UserRegisterView(CreateView):
    """
    Класс-представление для регистрации нового пользователя.

    Использует форму UserRegisterForm для создания нового пользователя.
    После успешной регистрации перенаправляет на страницу входа (login).

    Attributes:
        model: Класс модели User.
        form_class: Форма UserRegisterForm для создания нового пользователя.
        template_name: Имя шаблона для отображения страницы регистрации.
        success_url: URL для перенаправления после успешной регистрации.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register.html"
    success_url = reverse_lazy("users:login")


class ProfileView(UpdateView):
    """
    Класс-представление для редактирования профиля пользователя.

    Использует форму UserProfileForm для изменения данных пользователя.
    После успешного обновления профиля перенаправляет на страницу профиля (profile).

    Attributes:
        model: Класс модели User.
        form_class: Форма UserProfileForm для редактирования профиля пользователя.
        success_url: URL для перенаправления после успешного обновления профиля.
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile_view(request):
    """
    Функция-представление для отображения профиля текущего пользователя.

    Пользователь должен быть аутентифицирован. Отображает шаблон 'profile.html'
    с данными о текущем пользователе.

    Args:
        request: Объект запроса HTTP.

    Returns:
        HTTP Response: Отображает страницу профиля пользователя.
    """
    return render(request, "users/profile.html", {"user": request.user})


def login_view(request):
    """
    Функция-представление для отображения страницы входа.

    Args:
        request: Объект запроса HTTP.

    Returns:
        HTTP Response: Отображает страницу входа пользователя.
    """
    return render(request, "users/login.html")


def register_view(request):
    """
    Функция-представление для отображения страницы регистрации.

    Args:
        request: Объект запроса HTTP.

    Returns:
        HTTP Response: Отображает страницу регистрации пользователя.
    """
    return render(request, "users/register.html")


@login_required
def logout_view(request):
    """
    Функция-представление для выхода пользователя из системы.

    Если метод запроса POST, происходит выход пользователя и перенаправление
    на страницу входа. В противном случае отображается страница выхода.

    Args:
        request: Объект запроса HTTP.

    Returns:
        HTTP Response: Перенаправляет на страницу входа или отображает страницу выхода.
    """
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    return render(request, "users/logout.html")


class SubscriptionCreate(CreateView):

    def get(self, request, *args, **kwargs):
        """
            Обрабатывает GET-запрос пользователя для создания и обработки платежа через Stripe.

            Args:
            - request (HttpRequest): HTTP-запрос от пользователя.
            - *args: Позиционные аргументы для дополнительной обработки.
            - **kwargs: Именованные аргументы для дополнительной обработки.

            Returns:
            - HttpResponse: Перенаправляет пользователя на страницу оплаты Stripe.

            Raises:
            - PermissionDenied: Если у пользователя уже есть оформленный платеж.
        """
        if request.user.payments:
            raise PermissionDenied
        else:
            user = User.objects.get(pk=request.user.pk)
            payment = Subscription.objects.create(payment_data=datetime.now())
            create_stripe_product(payment.pk, payment.payment_data)
            price = create_stripe_price()
            session_id, payment_url = create_stripe_session(price)
            payment.session_id = session_id
            payment.payment_url = payment_url
            user.payment = payment
            user.save()
            payment.save()
            return redirect(payment.payment_url)
