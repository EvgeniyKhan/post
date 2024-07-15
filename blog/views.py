from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import BlogForm, BlogModeratorForm
from blog.models import Blog
from users.models import User, Subscription


class BlogCreateView(CreateView):
    model = Blog
    template_name = "blog/blog_form.html"
    fields = ("title", "content", "preview")
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
            new_content.user = self.request.user
            new_content.publish = True
            # Устанавливаем флаг платного контента в зависимости от статуса пользователя
            new_content.is_premium = self.request.user.payments or self.request.user.is_superuser
        new_content.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = "blog/blog_form.html"
    fields = "__all__"

    def get_form_class(self):
        """
            Возвращает соответствующий класс формы в зависимости от прав доступа пользователя и владения блог-постом.

            Возвращает:
            - BlogForm: Если текущий пользователь является владельцем блог-поста.
            - BlogModeratorForm: Если текущий пользователь имеет права на редактирование заголовка и содержимого блог-поста.

            Вызывает:
            - PermissionDenied: Если текущий пользователь не имеет достаточных прав или не является владельцем блог-поста.
        """
        user = self.object.owner
        if user == self.object.owner:
            return BlogForm
        if user.has_perm("blog.can_edit_title") and user.has_perm(
                "blog.can_edit_content"
        ):
            return BlogModeratorForm
        raise PermissionDenied


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    fields = ("title", "content")

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

    def get_context_data(self, **kwargs):
        """
            Добавляет дополнительные данные в контекст страницы блога.

            В контекст добавляется информация о доступе к контенту блога в зависимости от аутентификации пользователя и его подписки.

            Возвращает:
            - dict: Контекст данных страницы блога с дополнительной информацией о доступе к контенту.
        """
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        if self.request.user.is_authenticated or self.request.user == Blog.owner:
            user_subscribed = User.objects.filter(
                payments=self.request.user == Subscription.is_subscribed
            ).exists()
            if user_subscribed:
                context["can_view_content"] = True
            else:
                context["can_view_content"] = not blog.is_premium
        else:
            context["can_view_content"] = not blog.is_premium
        return context


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


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'blog_form.html', {'form': form})
