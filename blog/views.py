from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import BlogForm, BlogFormPremium
from blog.models import Blog
from users.models import Subscription
from users.services import check_payment_status
from django.core.exceptions import ObjectDoesNotExist


class BlogCreateView(CreateView):
    model = Blog
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")

    def get_context_data(self, **kwargs):
        """
        Получает дополнительные данные контекста для отображения формы создания блога.

        Args:
        **kwargs: Дополнительные аргументы ключевых слов, передаваемые в метод.

        Returns:
        dict: Словарь с дополнительными данными контекста для шаблона.
            Включает в себя заголовок страницы для создания блога.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание блога"
        return context

    def form_valid(self, form):
        """
        Метод при успешном создании.
        Если пользователь авторизован -
        Добавляет текущего пользователя при создании объекта.
        Меняет флаг публикации на положительный и определяет платный контент.
        """
        new_content = form.save(commit=False)
        if self.request.user.is_authenticated:
            new_content.owner = self.request.user  # Используйте 'owner' вместо 'user'
            new_content.publish = True
            # Устанавливаем флаг платного контента в зависимости от статуса пользователя
            new_content.is_premium = self.request.user.payments.exists() is not None or self.request.user.is_superuser
        new_content.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        try:
            subscription = Subscription.objects.get(pk=user.payments_id)
            if check_payment_status(subscription.content_id):
                return BlogFormPremium
            else:
                return BlogForm
        except ObjectDoesNotExist:
            return BlogForm


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "preview")
    success_url = reverse_lazy("blog:blog_list")

    def get_object(self, queryset=None):
        """
        Получает объект товара из базы данных и проверяет, является ли текущий пользователь владельцем товара.
        """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"

    def get_queryset(self):
        """
            Возвращает queryset блог-постов в зависимости от аутентификации пользователя и его прав.

            Если пользователь не аутентифицирован, возвращается queryset блог-постов,
            которые не являются премиумными.

            Если пользователь является суперпользователем или аутентифицирован, возвращается полный queryset
            всех блог-постов.

            Возвращает:
            - QuerySet: В зависимости от статуса аутентификации и прав пользователя,
              возвращается соответствующий QuerySet блог-постов.
        """
        if not self.request.user.is_authenticated:
            return Blog.objects.filter(is_premium=False)
        elif self.request.user.is_superuser or self.request.user.is_authenticated or check_payment_status(
                self.request.user.payments.content_id):
            return Blog.objects.all()


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """
            Возвращает объект блога для текущей страницы и обновляет счетчик просмотров.

            Args:
            - queryset (QuerySet, optional): QuerySet для поиска объекта блога.

            Returns:
            - Blog: Обновленный объект блога.
        """
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        return self.object

    def get_queryset(self):
        """
            Возвращает queryset блог-постов в зависимости от аутентификации пользователя и его прав.

            Если пользователь не аутентифицирован, возвращается queryset блог-постов,
            которые не являются премиумными.

            Если пользователь является суперпользователем или аутентифицирован, возвращается полный queryset
            всех блог-постов.

            Возвращает:
            - QuerySet: В зависимости от статуса аутентификации и прав пользователя,
            возвращается соответствующий QuerySet блог-постов.
        """
        if not self.request.user.is_authenticated:
            return Blog.objects.filter(is_premium=False)
        elif self.request.user.is_superuser or self.request.user.payments or self.request.user.is_authenticated:
            return Blog.objects.all()


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")

    def get_queryset(self):
        """
            Возвращает queryset блог-постов в зависимости от аутентификации пользователя и его прав.

            Если пользователь не аутентифицирован, возвращается queryset блог-постов,
            которые не являются премиумными.

            Если пользователь является суперпользователем или аутентифицирован, возвращается полный queryset
            всех блог-постов.

            Возвращает:
            - QuerySet: В зависимости от статуса аутентификации и прав пользователя,
            возвращается соответствующий QuerySet блог-постов.
        """
        if not self.request.user.is_authenticated:
            return Blog.objects.filter(is_premium=False)
        elif self.request.user.is_superuser or self.request.user.payments or self.request.user.is_authenticated:
            return Blog.objects.all()

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.owner or self.request.user.is_superuser


def subscription_required(request):
    return render(request, 'blog/blog_not_available.html')
