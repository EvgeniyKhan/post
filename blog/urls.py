from django.urls import path

from blog.apps import BlogConfig
from blog.views import (BlogCreateView, BlogDeleteView, BlogDetailView,
                        BlogListView, BlogUpdateView)

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("view/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete"),
    path("create/", BlogCreateView.as_view(), name="blog_create"),
]

"""
URL-шаблоны для управления блогами.

Includes URL patterns for listing, viewing, updating, deleting, and creating blog entries.

URL Patterns:
    '' (str): Список блогов.
    'view/<int:pk>/' (str): Просмотр конкретной статьи блога по идентификатору.
    'update/<int:pk>/' (str): Обновление конкретной статьи блога по идентификатору.
    'delete/<int:pk>/' (str): Удаление конкретной статьи блога по идентификатору.
    'create/' (str): Создание новой статьи блога.

Attributes:
    app_name (str): Имя приложения блога для пространства имен URL.
"""
