from django.forms import ModelForm

from blog.models import Blog
from users.forms import StyleFormMixin


class BlogForm(StyleFormMixin, ModelForm):
    """
    Форма для создания и редактирования блога.

    Наследуется от StyleFormMixin для добавления стилевых функций к форме.

    Attributes:
        Meta (class): Вложенный класс для определения метаинформации о форме.
            model (Model): Модель, с которой связана форма (Blog).
            fields (tuple): Поля модели, которые должны быть включены в форму
                (title, content, preview).
    """

    class Meta:
        """
        Метаинформация о форме для модели Blog.
        """

        model = Blog
        fields = ("title", "content", "preview")


class BlogModeratorForm(StyleFormMixin, ModelForm):
    """
    Форма для создания и редактирования блога.

    Наследуется от StyleFormMixin для добавления стилевых функций к форме.

    Attributes:
        Meta (class): Вложенный класс для определения метаинформации о форме.
            model (Model): Модель, с которой связана форма (Blog).
            fields (tuple): Поля модели, которые должны быть включены в форму
                (title, content, preview).
    """

    class Meta:
        """
        Метаинформация о форме для модели Blog.
        """

        model = Blog
        fields = ("title", "content")


class BlogFormPremium(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "content", "preview", "is_premium")
